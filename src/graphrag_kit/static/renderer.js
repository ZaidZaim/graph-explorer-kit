/* Graph renderer.
 *
 * Tries the Neo4j Visualization Library first. NVL is ESM-only with no UMD
 * build, so it comes from esm.sh — which means a live demo would be one CDN
 * outage away from a blank canvas. `createRenderer` therefore falls back to the
 * built-in canvas renderer below, which has no dependencies at all.
 *
 * Both implementations expose the same surface:
 *   setGraph({nodes, relationships})   replace the graph
 *   merge({nodes, relationships})      add nodes/edges not already present
 *   highlight(Set<id> | null)          dim everything outside the set
 *   select(id | null)                  mark one node as selected
 *   focus(id)                          centre the view on a node
 *   fit()                              zoom to fit
 */

const NVL_URL = 'https://esm.sh/@neo4j-nvl/base@1.2.1';
const NVL_INTERACTIONS_URL = 'https://esm.sh/@neo4j-nvl/interaction-handlers@1.2.1';

const STATUS_RING = { confirmed: '#2bd9c4', reported: '#ffc857', rumored: '#ff5a6e' };

export async function createRenderer(container, opts) {
  // Canvas is the default. NVL is the on-brand choice and stays available via
  // ?renderer=nvl, but it costs a ~10s cold fetch from esm.sh on first load and
  // puts a live demo at the mercy of a CDN. The canvas renderer has no
  // dependencies, starts instantly, and is styled for this palette.
  if (new URLSearchParams(location.search).get('renderer') === 'nvl') {
    try {
      return await createNvlRenderer(container, opts);
    } catch (err) {
      console.warn('NVL unavailable, using the built-in canvas renderer:', err.message);
    }
  }
  return createCanvasRenderer(container, opts);
}

/* =======================================================================
   NVL
   ======================================================================= */

async function createNvlRenderer(container, opts) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('NVL import timed out')), 8000));
  const [{ NVL }, interactions] = await Promise.race([
    Promise.all([import(NVL_URL), import(NVL_INTERACTIONS_URL)]),
    timeout,
  ]);

  const nvl = new NVL(container, [], [], {
    layout: 'forceDirected',
    initialZoom: 0.75,
    renderer: 'canvas',
    backgroundColor: '#120b1e',
  });

  // Guard the exact surface this adapter drives. NVL is pinned, but it is loaded
  // from a CDN at runtime: if the API ever shifts, fall back to canvas rather
  // than white-screening halfway through the first render.
  for (const method of ['addAndUpdateElementsInGraph', 'removeNodesWithIds', 'getNodes', 'fit']) {
    if (typeof nvl[method] !== 'function') {
      nvl.destroy?.();
      throw new Error(`NVL is missing ${method}()`);
    }
  }

  const { ZoomInteraction, PanInteraction, DragNodeInteraction, ClickInteraction } = interactions;
  new ZoomInteraction(nvl);
  new PanInteraction(nvl);
  new DragNodeInteraction(nvl);
  const click = new ClickInteraction(nvl);
  click.updateCallback('onNodeClick', (node) => opts.onNodeClick?.(node.id));
  click.updateCallback('onCanvasClick', () => opts.onBackgroundClick?.());

  let current = { nodes: [], relationships: [] };
  let highlighted = null;
  let selected = null;

  const toNvlNode = (n) => {
    const dim = highlighted && !highlighted.has(n.id);
    return {
      id: n.id,
      captions: [{ value: n.name }],
      caption: n.name,
      color: dim ? '#3a2c52' : (opts.colors[n.label] ?? '#8a8a8a'),
      size: n.id === selected ? 34 : 24,
      borderColor: STATUS_RING[n.status] ?? '#888',
      borderWidth: 3,
      selected: n.id === selected,
    };
  };
  const toNvlRel = (r) => ({
    id: r.id, from: r.from, to: r.to,
    captions: [{ value: r.type }], caption: r.type,
    color: 'rgba(255,255,255,0.28)',
  });

  const paint = () => {
    nvl.addAndUpdateElementsInGraph(current.nodes.map(toNvlNode), current.relationships.map(toNvlRel));
  };

  // NVL has no "replace the graph" call: clear by id, then add.
  const clear = () => {
    const ids = nvl.getNodes().map((n) => n.id);
    if (ids.length) nvl.removeNodesWithIds(ids);
  };
  const fitAll = () => {
    const ids = current.nodes.map((n) => n.id);
    if (ids.length) nvl.fit(ids);
  };

  return {
    kind: 'nvl',
    setGraph(graph) {
      current = graph;
      highlighted = null;
      selected = null;
      clear();
      paint();
      setTimeout(fitAll, 400);
    },
    merge(graph) {
      const ids = new Set(current.nodes.map((n) => n.id));
      const relIds = new Set(current.relationships.map((r) => r.id));
      current = {
        nodes: current.nodes.concat(graph.nodes.filter((n) => !ids.has(n.id))),
        relationships: current.relationships.concat(graph.relationships.filter((r) => !relIds.has(r.id))),
      };
      paint();
    },
    highlight(set) { highlighted = set; paint(); },
    select(id) { selected = id; paint(); },
    focus(id) { nvl.fit([id]); },
    fit: fitAll,
  };
}

/* =======================================================================
   Canvas fallback — force-directed, no dependencies
   ======================================================================= */

function createCanvasRenderer(container, opts) {
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;cursor:grab';
  container.appendChild(canvas);
  const ctx = canvas.getContext('2d');

  let nodes = [];          // {id,label,name,status,x,y,vx,vy,fixed}
  let edges = [];          // {from,to,type}
  let byId = new Map();
  let highlighted = null;
  let selected = null;

  const view = { scale: 0.9, x: 0, y: 0 };
  let dpr = 1;

  function resize() {
    dpr = window.devicePixelRatio || 1;
    const { clientWidth: w, clientHeight: h } = container;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
  }
  resize();
  new ResizeObserver(resize).observe(container);

  const toWorld = (sx, sy) => ({ x: (sx - view.x) / view.scale, y: (sy - view.y) / view.scale });

  /* ---- layout ---- */

  let alpha = 1;
  function step() {
    if (alpha > 0.002) {
      const k = 165;                      // preferred edge length
      // repulsion — O(n^2) is fine at this scale (~100 nodes)
      for (let i = 0; i < nodes.length; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < nodes.length; j++) {
          const b = nodes[j];
          let dx = b.x - a.x, dy = b.y - a.y;
          let d2 = dx * dx + dy * dy;
          if (d2 < 1) { dx = Math.random() - 0.5; dy = Math.random() - 0.5; d2 = 1; }
          const d = Math.sqrt(d2);
          const rep = (k * k * 1.5) / d2;
          const fx = (dx / d) * rep, fy = (dy / d) * rep;
          a.vx -= fx; a.vy -= fy;
          b.vx += fx; b.vy += fy;
        }
      }
      // springs
      for (const e of edges) {
        const a = byId.get(e.from), b = byId.get(e.to);
        if (!a || !b) continue;
        const dx = b.x - a.x, dy = b.y - a.y;
        const d = Math.hypot(dx, dy) || 1;
        const f = (d - k) * 0.02;
        const fx = (dx / d) * f, fy = (dy / d) * f;
        a.vx += fx; a.vy += fy;
        b.vx -= fx; b.vy -= fy;
      }
      // gravity toward origin, damping, integrate
      for (const n of nodes) {
        if (n.fixed) { n.vx = n.vy = 0; continue; }
        n.vx -= n.x * 0.006;
        n.vy -= n.y * 0.006;
        n.vx *= 0.86; n.vy *= 0.86;
        n.x += Math.max(-30, Math.min(30, n.vx)) * alpha;
        n.y += Math.max(-30, Math.min(30, n.vy)) * alpha;
      }
      alpha *= 0.994;
    }
    draw();
    requestAnimationFrame(step);
  }

  /* ---- drawing ---- */

  function draw() {
    const w = canvas.width / dpr, h = canvas.height / dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    ctx.save();
    ctx.translate(view.x, view.y);
    ctx.scale(view.scale, view.scale);

    const dim = (n) => highlighted && !highlighted.has(n.id);

    // edges
    ctx.lineWidth = 1.2 / view.scale;
    for (const e of edges) {
      const a = byId.get(e.from), b = byId.get(e.to);
      if (!a || !b) continue;
      const faded = dim(a) && dim(b);
      ctx.strokeStyle = faded ? 'rgba(255,255,255,0.05)' : 'rgba(255,255,255,0.20)';
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();

      if (!faded && view.scale > 0.55) {
        // arrowhead just short of the target node
        const ang = Math.atan2(b.y - a.y, b.x - a.x);
        const r = radius(b) + 4;
        const tx = b.x - Math.cos(ang) * r, ty = b.y - Math.sin(ang) * r;
        ctx.fillStyle = 'rgba(255,255,255,0.30)';
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(tx - Math.cos(ang - 0.4) * 9, ty - Math.sin(ang - 0.4) * 9);
        ctx.lineTo(tx - Math.cos(ang + 0.4) * 9, ty - Math.sin(ang + 0.4) * 9);
        ctx.closePath();
        ctx.fill();
      }

      if (view.scale > 1.15 && !faded) {
        ctx.save();
        ctx.font = `${9 / view.scale * 1}px "JetBrains Mono", monospace`;
        ctx.fillStyle = 'rgba(43,217,196,0.75)';
        ctx.textAlign = 'center';
        ctx.fillText(e.type, (a.x + b.x) / 2, (a.y + b.y) / 2 - 4);
        ctx.restore();
      }
    }

    // nodes
    for (const n of nodes) {
      const r = radius(n);
      const faded = dim(n);
      const base = opts.colors[n.label] ?? '#8a8a8a';

      if (n.id === selected) {
        ctx.beginPath();
        ctx.arc(n.x, n.y, r + 10, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255,77,157,0.22)';
        ctx.fill();
      }

      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fillStyle = faded ? 'rgba(58,44,82,0.55)' : base;
      ctx.fill();
      ctx.lineWidth = 2.5 / view.scale;
      ctx.strokeStyle = faded ? 'rgba(255,255,255,0.10)' : (STATUS_RING[n.status] ?? '#888');
      ctx.stroke();

      if (!faded || view.scale > 1) {
        ctx.font = `${11.5}px Inter, "Segoe UI", sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        const label = n.name.length > 26 ? n.name.slice(0, 25) + '…' : n.name;
        ctx.lineWidth = 3;
        ctx.strokeStyle = 'rgba(18,11,30,0.9)';
        ctx.strokeText(label, n.x, n.y + r + 5);
        ctx.fillStyle = faded ? 'rgba(242,233,255,0.35)' : '#f2e9ff';
        ctx.fillText(label, n.x, n.y + r + 5);
      }
    }
    ctx.restore();
  }

  const radius = (n) => (n.id === selected ? 17 : highlighted?.has(n.id) ? 15 : 12);

  /* ---- interaction ---- */

  let dragging = null, panning = false, last = null, moved = false;

  canvas.addEventListener('pointerdown', (ev) => {
    const rect = canvas.getBoundingClientRect();
    const p = toWorld(ev.clientX - rect.left, ev.clientY - rect.top);
    moved = false;
    const hit = pick(p.x, p.y);
    if (hit) { dragging = hit; hit.fixed = true; }
    else { panning = true; canvas.style.cursor = 'grabbing'; }
    last = { x: ev.clientX, y: ev.clientY };
    canvas.setPointerCapture(ev.pointerId);
  });

  canvas.addEventListener('pointermove', (ev) => {
    if (!last) {
      const rect = canvas.getBoundingClientRect();
      const p = toWorld(ev.clientX - rect.left, ev.clientY - rect.top);
      canvas.style.cursor = pick(p.x, p.y) ? 'pointer' : 'grab';
      return;
    }
    const dx = ev.clientX - last.x, dy = ev.clientY - last.y;
    if (Math.abs(dx) + Math.abs(dy) > 3) moved = true;
    if (dragging) {
      dragging.x += dx / view.scale;
      dragging.y += dy / view.scale;
      alpha = Math.max(alpha, 0.25);
    } else if (panning) {
      view.x += dx; view.y += dy;
    }
    last = { x: ev.clientX, y: ev.clientY };
  });

  canvas.addEventListener('pointerup', (ev) => {
    const rect = canvas.getBoundingClientRect();
    const p = toWorld(ev.clientX - rect.left, ev.clientY - rect.top);
    if (!moved) {
      const hit = pick(p.x, p.y);
      hit ? opts.onNodeClick?.(hit.id) : opts.onBackgroundClick?.();
    }
    if (dragging) dragging.fixed = false;
    dragging = null; panning = false; last = null;
    canvas.style.cursor = 'grab';
    canvas.releasePointerCapture(ev.pointerId);
  });

  canvas.addEventListener('wheel', (ev) => {
    ev.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const mx = ev.clientX - rect.left, my = ev.clientY - rect.top;
    const before = toWorld(mx, my);
    view.scale = Math.min(4, Math.max(0.12, view.scale * (ev.deltaY < 0 ? 1.12 : 1 / 1.12)));
    const after = toWorld(mx, my);
    view.x += (after.x - before.x) * view.scale;
    view.y += (after.y - before.y) * view.scale;
  }, { passive: false });

  function pick(x, y) {
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      if ((n.x - x) ** 2 + (n.y - y) ** 2 <= (radius(n) + 5) ** 2) return n;
    }
    return null;
  }

  function fit(subset) {
    const target = subset?.length ? subset : nodes;
    if (!target.length) return;
    const xs = target.map((n) => n.x), ys = target.map((n) => n.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    const minY = Math.min(...ys), maxY = Math.max(...ys);
    const w = canvas.width / dpr, h = canvas.height / dpr;
    // Leave room for the answer panel (top-left) and the ask bar (bottom).
    const padX = 130, padY = 150;
    view.scale = Math.min(2.2, Math.max(0.12,
      Math.min((w - padX * 2) / Math.max(1, maxX - minX), (h - padY * 2) / Math.max(1, maxY - minY))));
    view.x = w / 2 - ((minX + maxX) / 2) * view.scale;
    view.y = h / 2 - ((minY + maxY) / 2) * view.scale;
  }

  /* The force layout is still expanding when the first fit runs, so re-fit a few
     times as it cools rather than leaving nodes outside the viewport. */
  function fitWhileSettling() {
    for (const delay of [450, 1200, 2400]) setTimeout(() => fit(), delay);
  }

  function adopt(graph, keepPositions) {
    const previous = keepPositions ? byId : new Map();
    nodes = graph.nodes.map((n, i) => {
      const old = previous.get(n.id);
      const angle = (i / Math.max(1, graph.nodes.length)) * Math.PI * 2;
      return {
        ...n,
        x: old?.x ?? Math.cos(angle) * 260 + (Math.random() - 0.5) * 40,
        y: old?.y ?? Math.sin(angle) * 260 + (Math.random() - 0.5) * 40,
        vx: 0, vy: 0, fixed: false,
      };
    });
    byId = new Map(nodes.map((n) => [n.id, n]));
    edges = graph.relationships.filter((r) => byId.has(r.from) && byId.has(r.to));
    alpha = keepPositions ? 0.5 : 1;
  }

  requestAnimationFrame(step);

  return {
    kind: 'canvas',
    setGraph(graph) {
      highlighted = null; selected = null;
      adopt(graph, false);
      fitWhileSettling();
    },
    merge(graph) {
      const known = new Set(nodes.map((n) => n.id));
      const relIds = new Set(edges.map((r) => r.id));
      adopt({
        nodes: [...nodes, ...graph.nodes.filter((n) => !known.has(n.id))],
        relationships: [...edges, ...graph.relationships.filter((r) => !relIds.has(r.id))],
      }, true);
    },
    highlight(set) {
      highlighted = set;
      alpha = Math.max(alpha, 0.2);
      // Zoom to the evidence, so "here is where that answer came from" is a
      // visual statement rather than something the viewer has to hunt for.
      if (set?.size) setTimeout(() => fit(nodes.filter((n) => set.has(n.id))), 260);
    },
    select(id) { selected = id; },
    focus(id) {
      const n = byId.get(id);
      if (!n) return;
      const w = canvas.width / dpr, h = canvas.height / dpr;
      view.scale = Math.max(view.scale, 1.1);
      view.x = w / 2 - n.x * view.scale;
      view.y = h / 2 - n.y * view.scale;
    },
    fit,
  };
}

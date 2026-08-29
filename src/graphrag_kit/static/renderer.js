/* Graph renderer.
 *
 * Canvas is the default: no dependencies, instant start, full control over the
 * unfold animation. NVL is wired up behind ?renderer=nvl — it is the on-brand
 * choice but ships ESM-only, so it has to come from a CDN at runtime, which
 * costs a ~10s cold load and cannot drive the unfold.
 *
 * Public surface:
 *   setGraph({nodes, relationships})   replace the graph
 *   unfold({nodes, relationships, seeds})  reveal an answer's evidence
 *   collapse()                         return to the whole graph
 *   select(id | null)                  mark one node as selected
 *   focus(id)                          ease the view onto a node
 *   fit()                              zoom to fit
 */

const NVL_URL = 'https://esm.sh/@neo4j-nvl/base@1.2.1';
const NVL_INTERACTIONS_URL = 'https://esm.sh/@neo4j-nvl/interaction-handlers@1.2.1';

const STATUS_RING = { confirmed: '#2bd9c4', reported: '#ffc857', rumored: '#ff5a6e' };

// Unfold timing, milliseconds.
const RING_STAGGER = 190;   // delay added per depth ring
const NODE_FADE = 460;      // how long a node takes to arrive
const EDGE_DRAW = 340;      // how long an edge takes to draw itself
const RING_RADIUS = 190;    // minimum distance between depth rings
const NODE_ARC = 128;       // arc length each node needs on its ring, for labels
const RING_GAP = 150;       // minimum gap between consecutive rings
const GHOST_ALPHA = 0.09;   // what the rest of the graph fades to

const EDGE_BOW = 0.18;      // how far an edge bows away from a straight chord

const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
const easeInOutCubic = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
/** Per-frame lerp rate corrected for elapsed time, so easing takes the same
 *  wall-clock duration at 60fps and at 5fps. */
const rate = (perFrame, dt) => 1 - Math.pow(1 - perFrame, Math.max(dt, 1) / 16.67);

export async function createRenderer(container, opts) {
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
   Canvas — force-directed, with a radial unfold
   ======================================================================= */

function createCanvasRenderer(container, opts) {
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;cursor:grab';
  container.appendChild(canvas);
  const ctx = canvas.getContext('2d');

  let nodes = [];
  let edges = [];
  let byId = new Map();
  let selected = null;

  // Unfold state. `revealed` null means "showing the whole graph".
  let revealed = null;        // Set<id>
  let unfoldStart = 0;

  const view = { scale: 0.9, x: 0, y: 0 };
  const camera = { scale: 0.9, x: 0, y: 0, active: false };
  // Panels float over the canvas; fitting to the raw viewport centres the graph
  // underneath the answer card. These are set by the app as panels open/close.
  let insets = { left: 0, top: 0, right: 0, bottom: 0 };
  let dpr = 1;

  function resize() {
    dpr = window.devicePixelRatio || 1;
    canvas.width = container.clientWidth * dpr;
    canvas.height = container.clientHeight * dpr;
  }
  resize();
  new ResizeObserver(resize).observe(container);

  const size = () => ({ w: canvas.width / dpr, h: canvas.height / dpr });
  const toWorld = (sx, sy) => ({ x: (sx - view.x) / view.scale, y: (sy - view.y) / view.scale });

  /* ---- layout ---- */

  let alpha = 1;

  function physics() {
    if (alpha <= 0.002) return;
    const k = 165;
    const free = nodes.filter((n) => !n.pinned);

    for (let i = 0; i < free.length; i++) {
      const a = free[i];
      for (let j = i + 1; j < free.length; j++) {
        const b = free[j];
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
    for (const e of edges) {
      const a = byId.get(e.from), b = byId.get(e.to);
      if (!a || !b || a.pinned || b.pinned) continue;
      const dx = b.x - a.x, dy = b.y - a.y;
      const d = Math.hypot(dx, dy) || 1;
      const f = (d - k) * 0.02;
      a.vx += (dx / d) * f; a.vy += (dy / d) * f;
      b.vx -= (dx / d) * f; b.vy -= (dy / d) * f;
    }
    for (const n of free) {
      n.vx -= n.x * 0.006;
      n.vy -= n.y * 0.006;
      n.vx *= 0.86; n.vy *= 0.86;
      n.x += Math.max(-30, Math.min(30, n.vx)) * alpha;
      n.y += Math.max(-30, Math.min(30, n.vy)) * alpha;
    }
    alpha *= 0.994;
  }

  /** Ease pinned nodes toward their unfold targets, and advance appear/grow. */
  function animate(now, dt) {
    for (const n of nodes) {
      if (n.pinned && n.tx !== undefined) {
        // Each ring starts moving after the one inside it, so the graph opens
        // outward rather than everything sliding at once.
        const t = clamp01((now - unfoldStart - n.depth * RING_STAGGER) / NODE_FADE);
        const e = easeInOutCubic(t);
        n.x = n.fx + (n.tx - n.fx) * e;
        n.y = n.fy + (n.ty - n.fy) * e;
        n.appear = easeOutCubic(t);
      } else {
        const target = n.targetAppear ?? 1;
        n.appear += (target - n.appear) * rate(0.09, dt);
      }
    }
    for (const e of edges) {
      const a = byId.get(e.from), b = byId.get(e.to);
      if (!a || !b) continue;
      if (e.revealed) {
        const startAt = unfoldStart + (Math.max(a.depth ?? 0, b.depth ?? 0)) * RING_STAGGER + NODE_FADE * 0.55;
        e.grow = clamp01((now - startAt) / EDGE_DRAW);
      } else {
        const target = revealed ? 0 : 1;
        e.grow += (target - e.grow) * rate(0.09, dt);
      }
    }
    if (camera.active) {
      const k = rate(0.09, dt);
      view.scale += (camera.scale - view.scale) * k;
      view.x += (camera.x - view.x) * k;
      view.y += (camera.y - view.y) * k;
      if (Math.abs(camera.scale - view.scale) < 0.001 &&
          Math.abs(camera.x - view.x) < 0.5 && Math.abs(camera.y - view.y) < 0.5) {
        camera.active = false;
      }
    }
  }

  let lastFrame = performance.now();

  function step(now) {
    const dt = Math.min(now - lastFrame, 120);   // cap so a long stall is not one huge jump
    lastFrame = now;
    physics();
    animate(now, dt);
    draw();
  }

  function frame(now) {
    step(now);
    requestAnimationFrame(frame);
  }

  // Some embedded webviews report the document as permanently hidden, and
  // browsers pause requestAnimationFrame outright while hidden — which would
  // leave the graph frozen mid-unfold. This keeps it moving, at whatever rate
  // the host allows, and costs nothing when rAF is healthy.
  setInterval(() => {
    const now = performance.now();
    if (now - lastFrame > 200) step(now);
  }, 120);

  /* ---- unfold ---- */

  /** BFS from the seeds, then place each ring in its parent's angular sector. */
  function radialLayout(ids, seedIds) {
    const inSet = new Set(ids);
    const adj = new Map(ids.map((id) => [id, []]));
    for (const e of edges) {
      if (inSet.has(e.from) && inSet.has(e.to)) {
        adj.get(e.from).push(e.to);
        adj.get(e.to).push(e.from);
      }
    }
    const seeds = seedIds.filter((id) => inSet.has(id));
    const roots = seeds.length ? seeds : ids.slice(0, 1);

    const depth = new Map();
    const children = new Map(ids.map((id) => [id, []]));
    const queue = [];
    for (const r of roots) { depth.set(r, 0); queue.push(r); }
    // Any node the seeds cannot reach still gets placed, on an outer ring.
    for (let i = 0; i < queue.length; i++) {
      const cur = queue[i];
      for (const nb of adj.get(cur) ?? []) {
        if (!depth.has(nb)) {
          depth.set(nb, depth.get(cur) + 1);
          children.get(cur).push(nb);
          queue.push(nb);
        }
      }
    }
    const orphans = ids.filter((id) => !depth.has(id));
    const maxDepth = Math.max(0, ...[...depth.values()]);
    orphans.forEach((id) => depth.set(id, maxDepth + 1));

    // Leaf-count weighting keeps dense branches from overlapping thin ones.
    const weight = new Map();
    const weigh = (id) => {
      const kids = children.get(id) ?? [];
      const w = kids.length ? kids.reduce((s, c) => s + weigh(c), 0) : 1;
      weight.set(id, w);
      return w;
    };
    roots.forEach(weigh);

    // A ring holding N nodes needs circumference N*NODE_ARC, otherwise the
    // labels collide. Thirty seeds on a nominal inner ring is the common case
    // and looks like a single blob without this.
    const ringCount = new Map();
    for (const d of depth.values()) ringCount.set(d, (ringCount.get(d) ?? 0) + 1);
    const ringR = new Map();
    let previous = 0;
    for (const d of [...ringCount.keys()].sort((a, b) => a - b)) {
      const needed = (ringCount.get(d) * NODE_ARC) / (Math.PI * 2);
      const nominal = d === 0 ? 0 : previous + RING_GAP;
      const r = d === 0 && ringCount.get(0) === 1 ? 0 : Math.max(nominal, needed, d * RING_RADIUS);
      ringR.set(d, r);
      previous = r;
    }

    const pos = new Map();
    const place = (id, a0, a1) => {
      const d = depth.get(id);
      const mid = (a0 + a1) / 2;
      const r = ringR.get(d) ?? d * RING_RADIUS;
      pos.set(id, { x: Math.cos(mid) * r, y: Math.sin(mid) * r });
      const kids = children.get(id) ?? [];
      const total = kids.reduce((s, c) => s + (weight.get(c) ?? 1), 0) || 1;
      let a = a0;
      for (const c of kids) {
        const span = ((a1 - a0) * (weight.get(c) ?? 1)) / total;
        place(c, a, a + span);
        a += span;
      }
    };
    // Root sectors are weighted too: an even split starves a root carrying a
    // large subtree while a leaf root wastes its slice.
    const rootTotal = roots.reduce((s, r) => s + (weight.get(r) ?? 1), 0) || 1;
    let angle = 0;
    for (const r of roots) {
      const span = ((Math.PI * 2) * (weight.get(r) ?? 1)) / rootTotal;
      place(r, angle, angle + span);
      angle += span;
    }

    orphans.forEach((id, i) => {
      const ang = (i / Math.max(1, orphans.length)) * Math.PI * 2;
      const r = ringR.get(maxDepth + 1) ?? (maxDepth + 1) * RING_RADIUS;
      pos.set(id, { x: Math.cos(ang) * r, y: Math.sin(ang) * r });
    });
    return { pos, depth };
  }

  function easeCameraTo(subset, pad = 70) {
    const target = subset?.length ? subset : nodes;
    if (!target.length) return;
    const xs = target.map((n) => n.tx ?? n.x), ys = target.map((n) => n.ty ?? n.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    const minY = Math.min(...ys), maxY = Math.max(...ys);
    const { w, h } = size();

    // Usable area is the viewport minus whatever panels currently cover it.
    const availW = Math.max(200, w - insets.left - insets.right - pad * 2);
    const availH = Math.max(200, h - insets.top - insets.bottom - pad * 2);
    camera.scale = Math.min(1.9, Math.max(0.12, Math.min(
      availW / Math.max(1, maxX - minX),
      availH / Math.max(1, maxY - minY))));

    const cx = insets.left + pad + availW / 2;
    const cy = insets.top + pad + availH / 2;
    camera.x = cx - ((minX + maxX) / 2) * camera.scale;
    camera.y = cy - ((minY + maxY) / 2) * camera.scale;
    camera.active = true;
  }

  function unfold(graph) {
    mergeGraph(graph);
    const ids = graph.nodes.map((n) => n.id).filter((id) => byId.has(id));
    if (!ids.length) return;
    const seeds = (graph.seeds ?? []).filter((id) => byId.has(id));
    const { pos, depth } = radialLayout(ids, seeds);

    revealed = new Set(ids);
    unfoldStart = performance.now();

    for (const n of nodes) {
      if (revealed.has(n.id)) {
        const p = pos.get(n.id);
        n.depth = depth.get(n.id) ?? 0;
        n.isSeed = seeds.includes(n.id);
        n.fx = n.x; n.fy = n.y;      // where it starts from
        n.tx = p.x; n.ty = p.y;      // where it unfolds to
        n.pinned = true;
        n.appear = 0;
      } else {
        n.pinned = false;
        n.targetAppear = GHOST_ALPHA;
      }
    }
    for (const e of edges) {
      e.revealed = revealed.has(e.from) && revealed.has(e.to);
      if (e.revealed) e.grow = 0;
    }
    // Fit to where the nodes are going, not where they are now.
    setTimeout(() => easeCameraTo(nodes.filter((n) => revealed.has(n.id))), 80);
  }

  function collapse() {
    revealed = null;
    for (const n of nodes) {
      n.pinned = false;
      n.targetAppear = 1;
      n.depth = undefined;
      n.tx = n.ty = undefined;
      n.vx = n.vy = 0;
    }
    for (const e of edges) e.revealed = false;
    alpha = 0.55;                       // let the force layout re-settle
    setTimeout(() => easeCameraTo(nodes), 420);
  }

  /* ---- drawing ---- */

  /** Control point for an edge, perpendicular to the chord.
   *  Straight lines across a ring layout read as a ball of string; a consistent
   *  bow separates the two directions of a pair and follows the ring's curve. */
  function control(a, b) {
    const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
    const dx = b.x - a.x, dy = b.y - a.y;
    return { x: mx - dy * EDGE_BOW, y: my + dx * EDGE_BOW };
  }

  /** Stroke a quadratic from a to b, truncated at t via De Casteljau, so the
   *  edge can draw itself in during the unfold. */
  function strokeCurve(a, b, t) {
    const c = control(a, b);
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    if (t >= 0.999) {
      ctx.quadraticCurveTo(c.x, c.y, b.x, b.y);
    } else {
      const c1 = { x: a.x + (c.x - a.x) * t, y: a.y + (c.y - a.y) * t };
      const c2 = { x: c.x + (b.x - c.x) * t, y: c.y + (b.y - c.y) * t };
      const end = { x: c1.x + (c2.x - c1.x) * t, y: c1.y + (c2.y - c1.y) * t };
      ctx.quadraticCurveTo(c1.x, c1.y, end.x, end.y);
    }
    ctx.stroke();
  }

  const baseRadius = (n) => (n.id === selected ? 17 : n.isSeed && revealed ? 16 : 12);
  const radius = (n) => baseRadius(n) * (0.35 + 0.65 * Math.max(n.appear ?? 1, 0));

  function draw() {
    const { w, h } = size();
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    ctx.save();
    ctx.translate(view.x, view.y);
    ctx.scale(view.scale, view.scale);

    // edges
    for (const e of edges) {
      const a = byId.get(e.from), b = byId.get(e.to);
      if (!a || !b) continue;
      const g = e.grow ?? 1;
      if (g <= 0.01) continue;
      const lit = !revealed || e.revealed;
      ctx.lineWidth = (lit ? 1.5 : 1) / view.scale;
      ctx.strokeStyle = lit
        ? `rgba(255,255,255,${0.10 + 0.20 * g})`
        : `rgba(255,255,255,${0.05 * g})`;
      strokeCurve(a, b, g);

      if (lit && g > 0.98 && view.scale > 0.5) {
        const c = control(a, b);
        const ang = Math.atan2(b.y - c.y, b.x - c.x);   // tangent at the end
        const r = radius(b) + 4;
        const tx = b.x - Math.cos(ang) * r, ty = b.y - Math.sin(ang) * r;
        ctx.fillStyle = 'rgba(255,255,255,0.34)';
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(tx - Math.cos(ang - 0.4) * 9, ty - Math.sin(ang - 0.4) * 9);
        ctx.lineTo(tx - Math.cos(ang + 0.4) * 9, ty - Math.sin(ang + 0.4) * 9);
        ctx.closePath();
        ctx.fill();
      }
      if (lit && g > 0.98 && view.scale > 1.05) {
        ctx.save();
        ctx.font = `${9 / view.scale}px "JetBrains Mono", monospace`;
        ctx.fillStyle = 'rgba(43,217,196,0.75)';
        ctx.textAlign = 'center';
        // Midpoint of the quadratic, not of the chord.
        const c2 = control(a, b);
        ctx.fillText(e.type, 0.25 * a.x + 0.5 * c2.x + 0.25 * b.x,
                             0.25 * a.y + 0.5 * c2.y + 0.25 * b.y - 4);
        ctx.restore();
      }
    }

    // nodes
    for (const n of nodes) {
      const appear = n.appear ?? 1;
      if (appear <= 0.02) continue;
      const r = radius(n);
      const lit = !revealed || revealed.has(n.id);
      const base = opts.colors[n.label] ?? '#8a8a8a';

      if (lit && (n.id === selected || n.isSeed)) {
        ctx.beginPath();
        ctx.arc(n.x, n.y, r + 11, 0, Math.PI * 2);
        ctx.fillStyle = n.id === selected
          ? 'rgba(255,77,157,0.22)'
          : `rgba(255,77,157,${0.13 * appear})`;
        ctx.fill();
      }

      ctx.globalAlpha = lit ? Math.max(appear, 0.25) : appear;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fillStyle = lit ? base : '#3a2c52';
      ctx.fill();
      ctx.lineWidth = 2.5 / view.scale;
      ctx.strokeStyle = lit ? (STATUS_RING[n.status] ?? '#888') : 'rgba(255,255,255,0.10)';
      ctx.stroke();
      ctx.globalAlpha = 1;

      const showLabel = lit ? appear > 0.5 : view.scale > 1.2;
      if (showLabel) {
        ctx.globalAlpha = lit ? appear : 0.4;
        ctx.font = '11.5px Inter, "Segoe UI", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        const label = n.name.length > 26 ? n.name.slice(0, 25) + '…' : n.name;
        ctx.lineWidth = 3;
        ctx.strokeStyle = 'rgba(18,11,30,0.9)';
        ctx.strokeText(label, n.x, n.y + r + 5);
        ctx.fillStyle = '#f2e9ff';
        ctx.fillText(label, n.x, n.y + r + 5);
        ctx.globalAlpha = 1;
      }
    }
    ctx.restore();
  }

  /* ---- interaction ---- */

  let dragging = null, panning = false, last = null, moved = false;

  canvas.addEventListener('pointerdown', (ev) => {
    const rect = canvas.getBoundingClientRect();
    const p = toWorld(ev.clientX - rect.left, ev.clientY - rect.top);
    moved = false;
    const hit = pick(p.x, p.y);
    if (hit) { dragging = hit; hit.pinned = true; hit.tx = hit.ty = undefined; }
    else { panning = true; canvas.style.cursor = 'grabbing'; }
    camera.active = false;                 // a human gesture cancels the camera ease
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
    if (dragging && !revealed?.has(dragging.id)) dragging.pinned = false;
    dragging = null; panning = false; last = null;
    canvas.style.cursor = 'grab';
    canvas.releasePointerCapture(ev.pointerId);
  });

  canvas.addEventListener('wheel', (ev) => {
    ev.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const mx = ev.clientX - rect.left, my = ev.clientY - rect.top;
    const before = toWorld(mx, my);
    camera.active = false;
    view.scale = Math.min(4, Math.max(0.12, view.scale * (ev.deltaY < 0 ? 1.12 : 1 / 1.12)));
    const after = toWorld(mx, my);
    view.x += (after.x - before.x) * view.scale;
    view.y += (after.y - before.y) * view.scale;
  }, { passive: false });

  function pick(x, y) {
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      if ((n.appear ?? 1) < 0.15) continue;
      if ((n.x - x) ** 2 + (n.y - y) ** 2 <= (radius(n) + 6) ** 2) return n;
    }
    return null;
  }

  /* ---- graph state ---- */

  function adopt(graph, keepPositions) {
    const previous = keepPositions ? byId : new Map();
    nodes = graph.nodes.map((n, i) => {
      const old = previous.get(n.id);
      const angle = (i / Math.max(1, graph.nodes.length)) * Math.PI * 2;
      return {
        ...n,
        x: old?.x ?? Math.cos(angle) * 260 + (Math.random() - 0.5) * 40,
        y: old?.y ?? Math.sin(angle) * 260 + (Math.random() - 0.5) * 40,
        vx: 0, vy: 0,
        pinned: false,
        appear: old?.appear ?? 0,
        targetAppear: 1,
      };
    });
    byId = new Map(nodes.map((n) => [n.id, n]));
    edges = graph.relationships
      .filter((r) => byId.has(r.from) && byId.has(r.to))
      .map((r) => ({ ...r, grow: 0, revealed: false }));
    alpha = keepPositions ? 0.5 : 1;
  }

  function mergeGraph(graph) {
    const known = new Set(nodes.map((n) => n.id));
    const relIds = new Set(edges.map((r) => r.id));
    const fresh = graph.nodes.filter((n) => !known.has(n.id));
    const freshRels = graph.relationships.filter((r) => !relIds.has(r.id));
    if (!fresh.length && !freshRels.length) return;
    adopt({
      nodes: [...nodes, ...fresh],
      relationships: [...edges, ...freshRels],
    }, true);
  }

  // Browsers pause requestAnimationFrame entirely while the page is hidden, so
  // an unfold that starts in a background tab would otherwise be frozen
  // mid-flight when the viewer returns. Re-fit on the way back in.
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState !== 'visible') return;
    alpha = Math.max(alpha, 0.1);
    easeCameraTo(revealed ? nodes.filter((n) => revealed.has(n.id)) : nodes);
  });

  requestAnimationFrame(frame);

  return {
    kind: 'canvas',
    setGraph(graph) {
      revealed = null; selected = null;
      adopt(graph, false);
      for (const delay of [500, 1300, 2500]) setTimeout(() => easeCameraTo(nodes), delay);
    },
    unfold,
    collapse,
    setInsets(next) { insets = { left: 0, top: 0, right: 0, bottom: 0, ...next }; },
    debug: () => ({
      revealed: revealed ? revealed.size : null,
      nodes: nodes.length,
      pinned: nodes.filter((n) => n.pinned).length,
      rings: nodes.filter((n) => n.pinned).reduce((acc, n) => {
        const r = Math.round(Math.hypot(n.tx ?? 0, n.ty ?? 0));
        acc[n.depth] = acc[n.depth] ?? { count: 0, radius: r };
        acc[n.depth].count++;
        return acc;
      }, {}),
      view: { ...view }, insets: { ...insets },
    }),
    select(id) { selected = id; },
    focus(id) {
      const n = byId.get(id);
      if (!n) return;
      const { w, h } = size();
      camera.scale = Math.max(view.scale, 1.1);
      camera.x = w / 2 - n.x * camera.scale;
      camera.y = h / 2 - n.y * camera.scale;
      camera.active = true;
    },
    fit: () => easeCameraTo(nodes),
  };
}

/* =======================================================================
   NVL — same surface, no unfold (it owns its own layout)
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

  // Guard the exact surface this adapter drives: NVL is pinned but loaded from a
  // CDN, so fall back rather than white-screening mid-render if the API shifts.
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

  const paint = () =>
    nvl.addAndUpdateElementsInGraph(current.nodes.map(toNvlNode), current.relationships.map(toNvlRel));
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
      current = graph; highlighted = null; selected = null;
      clear(); paint();
      setTimeout(fitAll, 400);
    },
    unfold(graph) {
      const ids = new Set(graph.nodes.map((n) => n.id));
      const relIds = new Set(current.relationships.map((r) => r.id));
      current = {
        nodes: current.nodes.concat(graph.nodes.filter((n) => !current.nodes.some((c) => c.id === n.id))),
        relationships: current.relationships.concat(graph.relationships.filter((r) => !relIds.has(r.id))),
      };
      highlighted = ids;
      paint();
      setTimeout(() => nvl.fit([...ids]), 200);
    },
    collapse() { highlighted = null; paint(); fitAll(); },
    setInsets() { /* NVL owns its own viewport */ },
    select(id) { selected = id; paint(); },
    focus(id) { nvl.fit([id]); },
    fit: fitAll,
  };
}

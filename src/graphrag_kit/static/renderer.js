/* Graph renderer.
 *
 * Canvas is the default: no dependencies, instant start, full control over the
 * unfold animation. NVL is wired up behind ?renderer=nvl — it is the on-brand
 * choice but ships ESM-only, so it has to come from a CDN at runtime, which
 * costs a ~10s cold load and cannot drive the unfold.
 *
 * The unfold is staged, not one burst. /api/ask/stream sends a ring per
 * pipeline stage, and each one is added as it lands, so the picture grows in
 * the order the answer was actually reasoned out:
 *
 *     ( passage ) ──▶ ( entity ) ──▶ ( neighbour )
 *
 * Public surface:
 *   setGraph({nodes, relationships})       replace the graph
 *   beginUnfold()                          ghost the graph, ready for stage one
 *   addStage({nodes, relationships, stage}) reveal one more ring
 *   unfold({nodes, relationships})         begin + one stage, for one-shot views
 *   collapse()                             return to the whole graph
 *   select(id | null)                      mark one node as selected
 *   focus(id)                              ease the view onto a node
 *   fit()                                  zoom to fit
 */

const NVL_URL = 'https://esm.sh/@neo4j-nvl/base@1.2.1';
const NVL_INTERACTIONS_URL = 'https://esm.sh/@neo4j-nvl/interaction-handlers@1.2.1';

const STATUS_RING = { confirmed: '#4ADE80', reported: '#FFB454', rumored: '#FF5A6E' };

// Ground colour of the stage. Node labels are stroked in it so they stay
// readable over an edge, and ghosted nodes fade towards it.
const STAGE_BG = '#020616';
const GHOST_FILL = '#111a2b';
const ACCENT = '#6EE7FF';

const CHUNK_RING = 'rgba(110,231,255,0.55)';

// Unfold timing, milliseconds.
const NODE_FADE = 520;      // how long a node takes to arrive
const NODE_POP = 38;        // stagger between siblings arriving in one stage
const EDGE_DRAW = 380;      // how long an edge takes to draw itself
const GHOST_ALPHA = 0.07;   // what the rest of the graph fades to

// Fan geometry. The tree is rooted at the retrieved passages and opens to the
// right, so the picture reads the way the pipeline ran: what the question
// matched, then the entities in it, then what the graph reasoned over.
const FAN_SPREAD = Math.PI * 0.86;  // total angle the whole tree occupies
const RING_RADIUS = 190;    // nominal distance between depth rings
const RING_GAP = 150;       // minimum gap between consecutive rings
const NODE_ARC = 88;        // arc length each node needs, so labels do not collide
// Labels are drawn only where they can be read. Every node labelled at once is
// the single worst thing a dense graph view does to itself: a thousand names at
// four pixels of separation is a grey texture that hides the structure it is
// annotating. So a label needs either a sparse graph, or enough zoom that the
// node is genuinely big on screen — and whatever is under the pointer or
// selected is always named, so nothing is ever unidentifiable.
const LABEL_ALWAYS_BELOW = 40;   // nodes; below this, label everything
const LABEL_MIN_ON_SCREEN = 11;  // px radius a node needs before it gets a label

// A crowded ring is laid out as two interleaved rows rather than one enormous
// circle: it halves the radius the ring needs, which is the difference between
// a readable fan and a distant smudge.
const CROWDED = 14;         // nodes on a ring before it splits into two rows
const ROW_STAGGER = 46;     // radial offset between the two rows
const MIN_NODE_PX = 6;      // never let an *unfolded* node shrink below this

// Node size follows the size of the graph. A thousand records drawn at the
// radius that suits thirty is a solid mass of overlapping discs with no gaps
// for the edges to show through — which is the whole picture, since the edges
// are what make it a graph. Small graphs keep the full radius; a corpus-sized
// one becomes dots.
const NODE_RADIUS = 12;     // the radius a comfortable graph uses
const COMFORTABLE = 70;     // nodes; at or below this, full size
const DOT_MIN = 0.28;       // floor on the shrink factor

// Below this many nodes the view switches to the convention Neo4j Browser and
// Aura use: a big circle with its caption *inside* it, and every relationship
// drawn with its type and an arrowhead. It is the right way to read a graph you
// are actually studying — nothing has to be matched up with a legend, and the
// direction of each edge is on the edge. It only works while the circles are
// big enough to hold text, which is why it is a mode and not the only mode.
// Around thirty-five is the ceiling: sixty captioned circles fill the stage and
// each caption comes back to three characters, which is worse than no caption.
// The server's ring caps are set to land an unfold just under this.
const CAPTION_LIMIT = 36;     // nodes; at or below this, captions go inside
const CAPTION_RADIUS = 34;    // world radius in that mode
// The unfold lays its rings out on a fan whose arc-length budget per node is
// NODE_ARC, so a captioned circle there has to stay inside half of it.
const CAPTION_RADIUS_UNFOLD = 24;
const CAPTION_LINES = 3;      // most lines of caption a circle will hold
// Caption size follows the circle's size on screen rather than being fixed.
// A fixed size fits at one zoom and truncates every caption to four characters
// at any other — and how big the circles end up depends on the stage, the panel
// insets and how many nodes there are, none of which are known in advance.
const CAPTION_RATIO = 0.42;   // of the on-screen radius
const CAPTION_MIN_PX = 6.5;
const CAPTION_MAX_PX = 12;

const EDGE_BOW = 0.10;      // how far an edge bows away from a straight chord

const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
const easeInOutCubic = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
/** Per-frame lerp rate corrected for elapsed time, so easing takes the same
 *  wall-clock duration at 60fps and at 5fps. */
const rate = (perFrame, dt) => 1 - Math.pow(1 - perFrame, Math.max(dt, 1) / 16.67);

/** A darker cousin of a hex colour, for the ring around a node of that colour. */
function shade(hex, factor = 0.62) {
  const m = /^#?([0-9a-f]{6})$/i.exec(hex);
  if (!m) return hex;
  const v = parseInt(m[1], 16);
  const parts = [(v >> 16) & 255, (v >> 8) & 255, v & 255].map((c) =>
    Math.round(c * factor));
  return `rgb(${parts.join(',')})`;
}

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
   Canvas — force-directed at rest, a rooted fan while unfolding
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
  let stageOf = new Map();    // id -> the stage that introduced it
  let hovered = null;         // node under the pointer, always labelled
  // The ids the standing view asked for, remembered at setGraph. Anything in
  // `nodes` beyond this was merged in by an unfold or an ingest, belongs to that
  // one event, and goes back out when it ends. Without the record they
  // accumulate for the rest of the session: every answer used to leave its two
  // dozen entities behind, so a seventeen-node type overview became fifty-seven
  // nodes with arrows between them — and dropped out of caption mode, which
  // showed up as the labels moving outside the circles.
  let baseIds = new Set();

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

  /** Ideal separation, from the space available and the number of things in it.
   *
   *  A fixed spring length is fine for a demo corpus of thirty nodes and wrong
   *  for a thousand: repulsion then holds every pair apart at the same distance
   *  and the graph settles into an evenly spaced lattice, which is the least
   *  informative arrangement of a graph there is. Scaling with sqrt(area/n)
   *  keeps the whole graph roughly stage-sized whatever its size, which is what
   *  lets clusters read as clusters.
   */
  function spacing() {
    const { w, h } = size();
    const n = Math.max(nodes.length, 1);
    const area = Math.max(w * h, 1);
    const ideal = Math.max(34, Math.min(165, 0.9 * Math.sqrt(area / n)));
    // Captioned circles are much bigger than dots, so they need a floor of
    // their own: without it a fifty-node view packs radius-34 circles at a
    // spacing of seventy and they overlap. The multiplier leaves a gap of
    // roughly a circle between neighbours, which is where the relationship
    // types have to fit — pack them tighter and every type label collides with
    // a circle and is dropped.
    return captioned() ? Math.max(ideal, CAPTION_RADIUS * 3.3) : ideal;
  }

  /** Repulsion falls off as 1/d², so beyond a few multiples of the spacing it
   *  is noise. Bucketing by a grid of that size turns an O(n²) sweep into a
   *  handful of neighbour checks per node — at a thousand nodes the difference
   *  is a layout that settles in a second rather than a quarter of a million
   *  force calculations every frame. What the cutoff drops is global spread,
   *  and the centre gravity below already does that job. */
  const REPULSION_CUTOFF = 3;

  function physics() {
    if (alpha <= 0.002) return;
    const k = spacing();
    const free = nodes.filter((n) => !n.pinned);
    const cell = k * REPULSION_CUTOFF;
    const buckets = new Map();
    const key = (x, y) => `${Math.floor(x / cell)}:${Math.floor(y / cell)}`;
    for (const n of free) {
      const id = key(n.x, n.y);
      const bucket = buckets.get(id);
      if (bucket) bucket.push(n);
      else buckets.set(id, [n]);
    }

    const cutoff2 = cell * cell;
    for (const a of free) {
      const cx = Math.floor(a.x / cell), cy = Math.floor(a.y / cell);
      for (let ox = -1; ox <= 1; ox++) {
        for (let oy = -1; oy <= 1; oy++) {
          for (const b of buckets.get(`${cx + ox}:${cy + oy}`) ?? []) {
            // Each unordered pair is visited twice, once from each end, so the
            // force is applied to one node at a time rather than to both.
            if (b === a) continue;
            let dx = b.x - a.x, dy = b.y - a.y;
            let d2 = dx * dx + dy * dy;
            if (d2 > cutoff2) continue;
            if (d2 < 1) { dx = Math.random() - 0.5; dy = Math.random() - 0.5; d2 = 1; }
            const d = Math.sqrt(d2);
            const rep = (k * k * 1.5) / d2;
            a.vx -= (dx / d) * rep;
            a.vy -= (dy / d) * rep;
          }
        }
      }
    }
    for (const e of edges) {
      const a = byId.get(e.from), b = byId.get(e.to);
      if (!a || !b || a.pinned || b.pinned) continue;
      const dx = b.x - a.x, dy = b.y - a.y;
      const d = Math.hypot(dx, dy) || 1;
      const f = (d - k) * 0.035;
      a.vx += (dx / d) * f; a.vy += (dy / d) * f;
      b.vx -= (dx / d) * f; b.vy -= (dy / d) * f;
    }
    // Centre gravity, weaker the bigger the graph. It exists to stop
    // disconnected components drifting apart for ever, but at full strength on
    // a thousand nodes it packs every component into one ball and hides the
    // cluster structure that makes the picture worth looking at.
    const pull = nodes.length > 200 ? 0.004 : 0.012;
    for (const n of free) {
      n.vx -= n.x * pull;
      n.vy -= n.y * pull;
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
        // Every node carries its own start time, stamped by the stage that
        // introduced it — so a later stage can slide the earlier rings to their
        // new places without restarting their fade-in.
        const t = clamp01((now - n.animStart) / NODE_FADE);
        const e = easeInOutCubic(t);
        n.x = n.fx + (n.tx - n.fx) * e;
        n.y = n.fy + (n.ty - n.fy) * e;
        n.appear = n.animFrom + (1 - n.animFrom) * easeOutCubic(t);
      } else {
        const target = n.targetAppear ?? 1;
        n.appear += (target - n.appear) * rate(0.09, dt);
      }
    }
    for (const e of edges) {
      const a = byId.get(e.from), b = byId.get(e.to);
      if (!a || !b) continue;
      if (e.revealed) {
        e.grow = clamp01((now - (e.animStart ?? 0)) / EDGE_DRAW);
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

  /* ---- unfold layout ---- */

  /** Lay the revealed nodes out as a fan rooted at the question.
   *
   *  Depth comes from the stage that delivered a node, not from a walk of the
   *  edges, so the rings are exactly ask / passages / entities / neighbourhood
   *  even when an entity-to-entity edge would short-circuit the walk. A node's
   *  parent is the least-loaded neighbour one ring in, which stops the fan
   *  bunching everything under whichever passage happened to arrive first.
   */
  function flowLayout(ids) {
    const inSet = new Set(ids);
    const adj = new Map(ids.map((id) => [id, []]));
    for (const e of edges) {
      if (inSet.has(e.from) && inSet.has(e.to)) {
        adj.get(e.from).push(e.to);
        adj.get(e.to).push(e.from);
      }
    }

    const depth = new Map();
    for (const id of ids) depth.set(id, stageOf.get(id) ?? 1);

    const byDepth = new Map();
    for (const id of ids) {
      const d = depth.get(id);
      if (!byDepth.has(d)) byDepth.set(d, []);
      byDepth.get(d).push(id);
    }
    const depths = [...byDepth.keys()].sort((a, b) => a - b);
    const roots = byDepth.get(depths[0]);

    // Parent assignment, ring by ring outward.
    const children = new Map(ids.map((id) => [id, []]));
    const parent = new Map();
    const leastLoaded = (candidates) =>
      candidates.reduce((best, o) =>
        (children.get(o).length < children.get(best).length ? o : best));

    for (const d of depths.slice(1)) {
      let inner = [];
      for (const prev of depths) {
        if (prev >= d) break;
        inner = byDepth.get(prev);
      }
      for (const id of byDepth.get(d)) {
        const linked = (adj.get(id) ?? []).filter((o) => depth.get(o) < d);
        // No edge to an inner ring means the retrieval reached it some other
        // way; hang it off the emptiest inner node rather than dropping it.
        const par = linked.length ? leastLoaded(linked)
                  : inner.length ? leastLoaded(inner)
                  : roots[0];
        if (par === undefined || par === id) continue;
        parent.set(id, par);
        children.get(par).push(id);
      }
    }

    // Leaf-count weighting keeps dense branches from overlapping thin ones.
    const weight = new Map();
    const weigh = (id) => {
      const kids = children.get(id) ?? [];
      const w = kids.length ? kids.reduce((s, c) => s + weigh(c), 0) : 1;
      weight.set(id, w);
      return w;
    };
    roots.forEach(weigh);

    // A ring holding N nodes across FAN_SPREAD radians needs N*NODE_ARC of arc
    // length, or the labels collide. Thirty entities on a nominal ring is the
    // common case and reads as one blob without this.
    const ringR = new Map();
    const ringRows = new Map();
    const ringStagger = new Map();
    let previous = 0;
    for (const d of depths) {
      const count = byDepth.get(d).length;
      const rows = count > CROWDED ? 2 : 1;
      // A captioned ring needs only enough arc to clear the circles themselves;
      // NODE_ARC is sized for labels sitting *outside* the nodes, which spreads
      // the fan half again as wide as it has to be — and since the whole fan is
      // then fitted to the stage, that spread comes straight off how big each
      // circle ends up on screen.
      const arc = captioned() ? CAPTION_RADIUS_UNFOLD * 2.6 : NODE_ARC;
      const needed = (count * arc) / (FAN_SPREAD * rows);
      // Likewise the gap between rings and the stagger between a crowded ring's
      // two rows: both were sized to clear labels hanging below radius-12 dots,
      // and a radius-24 captioned circle needs the stagger to clear its own
      // diameter — at the old 46 the two rows overlapped — but far less gap.
      const gap = captioned() ? CAPTION_RADIUS_UNFOLD * 3.4 : RING_GAP;
      const step = captioned() ? CAPTION_RADIUS_UNFOLD * 5 : RING_RADIUS;
      const stagger = captioned() ? CAPTION_RADIUS_UNFOLD * 2.4 : ROW_STAGGER;
      const isHub = d === depths[0] && count === 1;
      const r = isHub
        ? 0
        : Math.max(previous + gap, (d - depths[0]) * step, needed);
      ringR.set(d, r);
      ringRows.set(d, rows);
      ringStagger.set(d, stagger);
      previous = r + (rows > 1 ? stagger : 0);
    }

    // In a wide, short area the fan is laid out as rows rather than rings: the
    // passages along the top, the entities under them, the neighbourhood along
    // the bottom. A fan with a 155-degree spread does not survive being turned
    // to open downward — its outer rings curl up to the height of the inner one
    // and the three depths collapse into a single jumbled band. Rows keep the
    // order the pipeline ran in readable top to bottom, and use the width.
    //
    // The sector-to-x mapping is shared by every row, so children sit under
    // their parents; it is scaled so the widest row still gets `arc` per node.
    const { w: cw, h: ch } = size();
    const layered = cw > ch * 1.3;
    const arcPer = captioned() ? CAPTION_RADIUS_UNFOLD * 2.6 : NODE_ARC;
    let widest = 0;
    for (const d of depths) {
      const count = byDepth.get(d).length;
      widest = Math.max(widest, (count * arcPer) / (ringRows.get(d) ?? 1));
    }
    const xScale = widest / FAN_SPREAD;
    const layerGap = captioned() ? CAPTION_RADIUS_UNFOLD * 5.2 : RING_GAP;
    // Crowded rows alternate nodes up and down; the offset is chosen so two
    // neighbours a half-arc apart horizontally still clear each other.
    const layerStagger = captioned() ? CAPTION_RADIUS_UNFOLD * 1.15 : ROW_STAGGER * 0.6;
    const depthIndex = new Map(depths.map((d, i) => [d, i]));

    const pos = new Map();
    const placedInRing = new Map(depths.map((d) => [d, 0]));
    const place = (id, a0, a1) => {
      const d = depth.get(id);
      const mid = (a0 + a1) / 2;
      const i = placedInRing.get(d) ?? 0;
      placedInRing.set(d, i + 1);
      // Siblings are placed consecutively, so alternating the radius puts
      // angular neighbours on different rows without disturbing the order.
      const base = ringR.get(d) ?? 0;
      const stagger = ringStagger.get(d) ?? ROW_STAGGER;
      const offset = ringRows.get(d) > 1 ? (i % 2 ? stagger : -stagger) : 0;
      const r = base > 0 ? base + offset : 0;
      if (layered) {
        const row = depthIndex.get(d) ?? 0;
        const stag = ringRows.get(d) > 1 ? (i % 2 ? layerStagger : -layerStagger) : 0;
        pos.set(id, { x: mid * xScale, y: row * layerGap + stag });
      } else {
        pos.set(id, { x: Math.cos(mid) * r, y: Math.sin(mid) * r });
      }

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
    let angle = -FAN_SPREAD / 2;
    for (const r of roots) {
      const span = (FAN_SPREAD * (weight.get(r) ?? 1)) / rootTotal;
      place(r, angle, angle + span);
      angle += span;
    }
    return { pos, depth, parent };
  }

  // The first stage of an unfold holds one node. Fitting to its bounding box
  // would slam the camera to maximum zoom, then back out again as the rings
  // arrive; a floor on the extent keeps the opening shot steady.
  const MIN_EXTENT = 620;

  function easeCameraTo(subset, pad = null) {
    const target = subset?.length ? subset : nodes;
    if (!target.length) return;
    const xs = target.map((n) => n.tx ?? n.x), ys = target.map((n) => n.ty ?? n.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    const minY = Math.min(...ys), maxY = Math.max(...ys);
    const { w, h } = size();

    // Margin scaled to the viewport rather than a flat 70px. On a laptop-sized
    // stage — or a projector — a fixed margin on all four sides is a quarter of
    // the width spent on nothing, which squeezes the graph into the middle and
    // makes its labels collide. It still has to clear a node's label, which
    // hangs below the node, hence the floor.
    if (pad === null) pad = Math.max(26, Math.min(70, 0.055 * Math.min(w, h)));

    // Usable area is the viewport minus whatever panels currently cover it.
    // On a small stage the answer card and the ask bar can between them claim
    // more than the whole height; clamping the floor alone is not enough,
    // because the centre is then computed below the viewport and the graph is
    // drawn underneath the ask bar. Give the card's reservation up first — it
    // is translucent and scrollable, so a little overlap costs nothing, whereas
    // a graph hidden behind the input is simply gone.
    let reserveTop = insets.top;
    const MIN_USABLE = 190;
    if (h - reserveTop - insets.bottom < MIN_USABLE) {
      reserveTop = Math.max(0, h - insets.bottom - MIN_USABLE);
    }
    const availW = Math.max(200, w - insets.left - insets.right - pad * 2);
    const availH = Math.max(200, h - reserveTop - insets.bottom - pad * 2);
    camera.scale = Math.min(1.9, Math.max(0.12, Math.min(
      availW / Math.max(MIN_EXTENT, maxX - minX),
      availH / Math.max(MIN_EXTENT, maxY - minY))));

    const cx = insets.left + pad + availW / 2;
    const cy = reserveTop + pad + availH / 2;
    camera.x = cx - ((minX + maxX) / 2) * camera.scale;
    camera.y = cy - ((minY + maxY) / 2) * camera.scale;
    camera.active = true;
  }

  /* ---- unfold ---- */

  /** Start a fresh unfold: ghost the standing graph, ready for the first ring. */
  function beginUnfold() {
    revealed = new Set();
    stageOf = new Map();
    alpha = 0;                          // the ghosted graph stops drifting
    for (const e of edges) { e.revealed = false; }
    for (const n of nodes) {
      n.pinned = false;
      n.targetAppear = GHOST_ALPHA;
      n.tx = n.ty = undefined;
      n.depth = undefined;
      n.isSeed = false;
    }
  }

  /** Reveal one more ring. Nodes already on screen glide to their new places;
   *  the new ones grow out of their parent, staggered, and their edges draw
   *  themselves in behind them. */
  function addStage({ nodes: incoming = [], relationships = [], stage = 1 } = {}) {
    if (!revealed) beginUnfold();
    mergeGraph({ nodes: incoming, relationships });
    alpha = 0;

    const fresh = new Set();
    for (const n of incoming) {
      if (!byId.has(n.id) || revealed.has(n.id)) continue;
      revealed.add(n.id);
      stageOf.set(n.id, stage);
      fresh.add(n.id);
    }
    if (!revealed.size) return;

    const ids = [...revealed];
    const { pos, depth, parent } = flowLayout(ids);
    const now = performance.now();

    let popped = 0;
    for (const id of ids) {
      const n = byId.get(id);
      const p = pos.get(id);
      if (!n || !p) continue;
      if (fresh.has(id)) {
        // New nodes emerge from wherever their parent currently is, so the ring
        // visibly grows out of the one inside it rather than fading in on top.
        const par = parent.get(id) ? byId.get(parent.get(id)) : null;
        n.x = par ? par.x : p.x;
        n.y = par ? par.y : p.y;
        n.appear = 0;
        n.animFrom = 0;
        n.animStart = now + popped++ * NODE_POP;
      } else {
        n.animFrom = n.appear ?? 1;
        n.animStart = now;
      }
      n.depth = depth.get(id);
      n.isSeed = stageOf.get(id) === 1;
      n.pinned = true;
      n.fx = n.x; n.fy = n.y;
      n.tx = p.x; n.ty = p.y;
    }

    for (const e of edges) {
      const was = e.revealed;
      e.revealed = revealed.has(e.from) && revealed.has(e.to);
      if (e.revealed && !was) {
        const a = byId.get(e.from), b = byId.get(e.to);
        e.grow = 0;
        e.animStart =
          Math.max(a?.animStart ?? now, b?.animStart ?? now) + NODE_FADE * 0.45;
      }
    }

    // Fit to where the nodes are going, not where they are now.
    setTimeout(() => easeCameraTo(nodes.filter((n) => revealed?.has(n.id))), 60);
  }

  function collapse() {
    revealed = null;
    stageOf = new Map();
    // Back to exactly what the standing view asked for. Everything else was
    // merged in by the unfold — the retrieved passages, which were never graph
    // records at all, and the entities and neighbours it added on top.
    const transient = new Set(
      nodes.filter((n) => !baseIds.has(n.id)).map((n) => n.id));
    if (transient.size) {
      nodes = nodes.filter((n) => !transient.has(n.id));
      byId = new Map(nodes.map((n) => [n.id, n]));
      edges = edges.filter((e) => byId.has(e.from) && byId.has(e.to));
    }
    for (const n of nodes) {
      n.pinned = false;
      n.targetAppear = 1;
      n.depth = undefined;
      n.isSeed = false;
      n.tx = n.ty = undefined;
      n.vx = n.vy = 0;
    }
    for (const e of edges) e.revealed = false;
    alpha = 0.55;                       // let the force layout re-settle
    setTimeout(() => easeCameraTo(nodes), 420);
  }

  /* ---- drawing ---- */

  /** Control point for an edge, perpendicular to the chord.
   *  Straight lines across a fan read as a ball of string; a consistent bow
   *  separates the two directions of a pair and follows the ring's curve. */
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

  /** ctx.roundRect is recent enough that a fallback is cheaper than a probe. */
  function roundRectPath(x, y, w, h, r) {
    const rad = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    if (ctx.roundRect) { ctx.roundRect(x, y, w, h, rad); return; }
    ctx.moveTo(x + rad, y);
    ctx.arcTo(x + w, y, x + w, y + h, rad);
    ctx.arcTo(x + w, y + h, x, y + h, rad);
    ctx.arcTo(x, y + h, x, y, rad);
    ctx.arcTo(x, y, x + w, y, rad);
    ctx.closePath();
  }

  const isChunk = (n) => n.label === 'Chunk';

  /** Whether to draw Browser-style: caption inside the circle, typed edges.
   *
   *  During an unfold only the revealed rings count — the ghosted graph behind
   *  them may be a thousand nodes, and they are not what is being read. That is
   *  what lets an answer's evidence be as legible as the type overview: the
   *  rings are capped server-side precisely so they fit here.
   */
  const captioned = () =>
    (revealed ? revealed.size : nodes.length) <= CAPTION_LIMIT;

  const captionRadius = () => (revealed ? CAPTION_RADIUS_UNFOLD : CAPTION_RADIUS);

  /** Shrink factor for the current graph size, 1 for anything comfortable. */
  function nodeScale() {
    const n = Math.max(nodes.length, 1);
    return Math.max(DOT_MIN, Math.min(1, Math.sqrt(COMFORTABLE / n)));
  }

  const baseRadius = (n) => {
    // An explicit radius means the view is encoding something in the size — the
    // record count, in the type views — so it is scaled but never overridden.
    // In caption mode it is only ever grown, never shrunk below what the text
    // needs, or the caption would not fit in the thing it names.
    const explicit = n.radius;
    const nominal = explicit ?? (n.id === selected ? 17 : isChunk(n) ? 15 : NODE_RADIUS);
    // Ghosted nodes never get the caption radius: during an unfold they are the
    // faint backdrop, and inflating a thousand of them to 34 units would bury
    // the rings the unfold exists to show.
    const ghosted = revealed && !revealed.has(n.id);
    if (captioned() && !ghosted) return Math.max(explicit ?? 0, captionRadius());
    return nominal * nodeScale();
  };
  /** Grown by `appear` on the way in, and floored so a wide fan zoomed out to
   *  fit is still made of visible dots rather than dust. */
  const radius = (n) => {
    // The screen-size floor is for the unfold only: applying it to the ghosted
    // graph turns a faint backdrop into a field of grey dots competing with it.
    const ghost = revealed && !revealed.has(n.id);
    // The screen-size floor is for the unfold only. Applied to the standing
    // graph it undoes the shrink above: at half zoom it forces every node back
    // to twelve world units, and a thousand of those is the packed disc this
    // was meant to avoid.
    const base = revealed && !ghost
      ? Math.max(baseRadius(n), MIN_NODE_PX / view.scale)
      : baseRadius(n);
    return base * (0.35 + 0.65 * Math.max(n.appear ?? 1, 0));
  };

  function draw() {
    const { w, h } = size();
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    ctx.save();
    ctx.translate(view.x, view.y);
    ctx.scale(view.scale, view.scale);

    // edges
    const edgeLabels = [];
    for (const e of edges) {
      const a = byId.get(e.from), b = byId.get(e.to);
      if (!a || !b) continue;
      const g = e.grow ?? 1;
      if (g <= 0.01) continue;
      const lit = !revealed || e.revealed;
      // An edge out of a passage is the retrieval's own work rather than a fact
      // the graph already held, so it reads warmer than the rest.
      const flow = lit && (isChunk(a) || isChunk(b));
      // Edges thin and fade as the graph grows. Eight hundred of them at the
      // weight that suits eighty overlap into a solid white mass in the middle,
      // which reads as one bright blob rather than as connections — the nodes
      // disappear behind their own edges.
      const dense = nodes.length > 200;
      ctx.lineWidth = (flow ? 1.8 : lit ? (dense ? 0.85 : 1.5) : 1) / view.scale;
      ctx.strokeStyle = flow
        ? `rgba(110,231,255,${0.18 + 0.38 * g})`
        : lit
        ? `rgba(196,214,236,${(dense ? 0.05 + 0.08 * g : 0.10 + 0.20 * g)})`
        : `rgba(255,255,255,${0.05 * g})`;
      strokeCurve(a, b, g);

      if (lit && g > 0.98 && (captioned() || view.scale > 0.5)) {
        const c = control(a, b);
        const ang = Math.atan2(b.y - c.y, b.x - c.x);   // tangent at the end
        const r = radius(b) + 4;
        const tx = b.x - Math.cos(ang) * r, ty = b.y - Math.sin(ang) * r;
        ctx.fillStyle = flow ? 'rgba(110,231,255,0.65)' : 'rgba(196,214,236,0.42)';
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(tx - Math.cos(ang - 0.4) * 9, ty - Math.sin(ang - 0.4) * 9);
        ctx.lineTo(tx - Math.cos(ang + 0.4) * 9, ty - Math.sin(ang + 0.4) * 9);
        ctx.closePath();
        ctx.fill();
      }
      // The relationship type, on the relationship. Previously this needed
      // view.scale > 1.05, which a graph fitted to the stage never reaches — so
      // the types were effectively never drawn. Now they appear whenever the
      // graph is small enough to be read, which is the case that wants them.
      // Collected rather than drawn: they have to be placed after the node
      // captions, so that a type never lands on top of a node's own name.
      if (lit && g > 0.98 && (captioned() || view.scale > 1.05)) {
        // Midpoint of the quadratic, not of the chord.
        const c2 = control(a, b);
        edgeLabels.push({
          text: e.type,
          x: 0.25 * a.x + 0.5 * c2.x + 0.25 * b.x,
          y: 0.25 * a.y + 0.5 * c2.y + 0.25 * b.y,
          weight: e.properties?.count ?? 0,
          flow,
        });
      }
    }

    // nodes
    const deferredLabels = [];
    const reserved = [];
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
          ? 'rgba(110,231,255,0.24)'
          : `rgba(110,231,255,${0.14 * appear})`;
        ctx.fill();
      }

      ctx.globalAlpha = lit ? Math.max(appear, 0.25) : appear;
      // Passages are squares and entities are circles: the ring a node belongs
      // to is then readable without following the edges back to the question.
      if (isChunk(n)) {
        const s = r * 1.7;
        roundRectPath(n.x - s / 2, n.y - s / 2, s, s, 5);
      } else {
        ctx.beginPath();
        ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      }
      ctx.fillStyle = lit ? base : GHOST_FILL;
      ctx.fill();
      // A 2.5px ring on a 4px dot is mostly ring. Keep it proportional.
      ctx.lineWidth = Math.min(2.5, r * 0.34) / view.scale;
      // The ring carries the evidence level where the corpus grades one. Where
      // it does not, a single grey ring on every node is noise pretending to be
      // information, so the node's own colour is deepened instead.
      ctx.strokeStyle = lit
        ? (isChunk(n) ? CHUNK_RING : STATUS_RING[n.status] ?? shade(base))
        : 'rgba(255,255,255,0.10)';
      ctx.stroke();
      ctx.globalAlpha = 1;

      // Browser-style: the caption lives inside the circle it names, so there
      // is nothing to match up against a legend and nothing to collide with.
      if (captioned() && lit) {
        const box = drawCaptionInside(n, r, base, 1);
        // The circle itself is reserved, not just the text: a relationship type
        // printed across a node reads as that node's label.
        reserved.push(box ?? screenBox(n.x, n.y, r * 1.9, r * 1.9));
        // A circle too small on screen to hold its caption is not left nameless:
        // it gets the ordinary label underneath instead, subject to the usual
        // collision rules. This is what a small window or a high zoom level
        // sees, and a nameless circle there is worse than a crowded one.
        if (box) continue;
      }

      // Ghosted nodes never label themselves during an unfold — the point of
      // ghosting is to get the rest of the graph out of the way. Inside the
      // unfold, the outer rings drop their labels once the view is wide enough
      // that they would only overlap each other.
      // Each ring out needs more zoom before its labels are worth the clutter:
      // the passages and their entities carry the answer, the outer ring is
      // context you go looking for.
      const needed = revealed ? [0, 0, 0.42, 0.7][Math.min(n.depth ?? 3, 3)] : 0;
      const readable =
        nodes.length <= LABEL_ALWAYS_BELOW || r * view.scale >= LABEL_MIN_ON_SCREEN;
      const named = n.id === hovered || n.id === selected;
      const showLabel = lit
        ? (named || (appear > 0.5 && view.scale > needed && readable))
        : !revealed && view.scale > 1.2;
      // Labels are all held back to a second pass: they need to land on top of
      // every node, and they need to know about each other.
      if (showLabel) deferredLabels.push({ n, r, alpha: lit ? appear : 0.4, named });
    }

    drawEdgeLabels(edgeLabels, reserved);
    drawLabels(deferredLabels);
    ctx.restore();
  }

  /** A screen-space box around a world-space centre. */
  function screenBox(x, y, w, h) {
    return {
      x: x * view.scale + view.x - (w * view.scale) / 2,
      y: y * view.scale + view.y - (h * view.scale) / 2,
      w: w * view.scale,
      h: h * view.scale,
    };
  }

  const overlaps = (a, b) =>
    a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;

  /** Relationship types, heaviest first, skipping any that would collide.
   *
   *  Every edge labelled is how the middle of a hub-and-spoke graph turns into
   *  a pile of overstruck words: fourteen MENTIONS edges leave Document, and
   *  their midpoints are all in the same small area. Placing them in weight
   *  order means the labels that survive are the ones standing for the most
   *  relationships. */
  function drawEdgeLabels(candidates, reserved) {
    if (!candidates.length) return;
    const px = (v) => v / view.scale;
    candidates.sort((a, b) => b.weight - a.weight);
    const placed = [...reserved];
    ctx.save();
    ctx.font = `${px(8.5)}px "IBM Plex Mono", ui-monospace, monospace`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    for (const item of candidates) {
      const w = ctx.measureText(item.text).width;
      const box = screenBox(item.x, item.y, w + px(6), px(12));
      if (placed.some((other) => overlaps(box, other))) continue;
      placed.push(box);
      // Stroked in the stage colour so the line does not run through the
      // middle of the word.
      ctx.lineWidth = px(3.5);
      ctx.strokeStyle = STAGE_BG;
      ctx.strokeText(item.text, item.x, item.y);
      ctx.fillStyle = item.flow ? 'rgba(110,231,255,0.9)' : 'rgba(148,170,196,0.95)';
      ctx.fillText(item.text, item.x, item.y);
    }
    ctx.restore();
  }

  /** Draw as many labels as fit without overlapping each other.
   *
   *  Gating on zoom stops a thousand labels being drawn at once, but it cannot
   *  stop the dozen that *are* drawn from landing on top of one another —
   *  neighbouring nodes are neighbouring precisely because they are close. So
   *  labels are placed greedily, biggest node first, and one that would collide
   *  with a label already placed is dropped. The set thins out as things get
   *  tight instead of turning into overstruck mush, and whatever is under the
   *  pointer is placed first, so it is never the one dropped.
   */
  function drawLabels(candidates) {
    if (!candidates.length) return;
    // Hovered and selected first, then the most connected, then the biggest.
    candidates.sort((a, b) =>
      (b.named - a.named) ||
      ((b.n.degree ?? 0) - (a.n.degree ?? 0)) ||
      (b.r - a.r));
    const placed = [];
    const gap = 2;
    for (const item of candidates) {
      const { n, r, alpha, named } = item;
      ctx.font = `${(named ? 11.5 : 10.5) / view.scale}px "IBM Plex Mono", ui-monospace, monospace`;
      const text = n.name.length > 34 ? n.name.slice(0, 33) + '…' : n.name;
      // Screen space, because that is where the collisions happen: the world
      // gap between two nodes shrinks with the zoom, the text does not.
      const w = ctx.measureText(text).width * view.scale + gap * 2;
      const h = 13 + gap * 2;
      const x = n.x * view.scale + view.x - w / 2;
      const y = (n.y + r) * view.scale + view.y + 4;
      const clash = placed.some(
        (p) => x < p.x + p.w && x + w > p.x && y < p.y + p.h && y + h > p.y);
      if (clash && !named) continue;
      placed.push({ x, y, w, h });
      drawLabel(n, r, alpha, named);
    }
  }

  /** Break a caption into lines that fit inside a circle of radius `r`.
   *
   *  The usable width is taken as a chord rather than the diameter, because
   *  text set to the full width of a circle overhangs it at the top and bottom
   *  lines. Words longer than a line are cut with an ellipsis rather than
   *  overflowing, and a caption too long for `CAPTION_LINES` ends in one.
   */
  function wrapCaption(text, r, font) {
    ctx.font = font;
    const width = r * 1.55;
    const words = String(text ?? '').split(/\s+/).filter(Boolean);
    const lines = [];
    let line = '';
    const fits = (candidate) => ctx.measureText(candidate).width <= width;

    for (const word of words) {
      const candidate = line ? `${line} ${word}` : word;
      if (fits(candidate)) { line = candidate; continue; }
      if (line) lines.push(line);
      if (lines.length === CAPTION_LINES) { line = ''; break; }
      // A single word wider than the line gets truncated to fit.
      line = word;
      if (!fits(line)) {
        let cut = word;
        while (cut.length > 1 && !fits(`${cut}…`)) cut = cut.slice(0, -1);
        line = `${cut}…`;
      }
    }
    if (line && lines.length < CAPTION_LINES) lines.push(line);
    if (lines.length === CAPTION_LINES && words.length) {
      // Mark that something was dropped, rather than ending mid-thought.
      const joined = lines.join(' ');
      if (joined.length < String(text).length && !lines[lines.length - 1].endsWith('…')) {
        let last = lines[lines.length - 1];
        while (last.length > 1 && !fits(`${last}…`)) last = last.slice(0, -1);
        lines[lines.length - 1] = `${last}…`;
      }
    }
    return lines;
  }

  /** Relative luminance of a fill, for choosing readable text over it. */
  function isLight(color) {
    const m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(color);
    if (!m) return false;
    const [r, g, b] = m.slice(1).map((h) => parseInt(h, 16) / 255);
    return 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.55;
  }

  /** The caption, centred inside its own circle. */
  function drawCaptionInside(n, r, fill, alpha) {
    const px = (v) => v / view.scale;
    const onScreen = r * view.scale;
    const size = Math.max(CAPTION_MIN_PX, Math.min(CAPTION_MAX_PX, onScreen * CAPTION_RATIO));
    // Below this the text would be unreadable anyway, and a circle full of
    // grey mush is worse than a plain circle.
    if (onScreen < 11) return null;
    const font = `${px(size)}px "IBM Plex Mono", ui-monospace, monospace`;
    const lines = wrapCaption(n.name, r, font);
    if (!lines.length) return null;
    const lineHeight = px(size * 1.3);
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.font = font;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    // Dark text on the light fills, light text on the dark ones, so every
    // POLE colour stays readable without a second palette.
    ctx.fillStyle = isLight(fill) ? 'rgba(2,6,22,0.92)' : 'rgba(255,255,255,0.94)';
    const top = n.y - ((lines.length - 1) * lineHeight) / 2;
    lines.forEach((line, i) => ctx.fillText(line, n.x, top + i * lineHeight));
    ctx.restore();
    return screenBox(n.x, n.y, r * 1.9, r * 1.9);
  }

  /** One node label, stroked in the stage colour so it survives over an edge.
   *
   *  Sized in *screen* pixels, not world units: the canvas is drawn inside a
   *  scaled transform, so a plain `10.5px` font shrinks with the zoom and a
   *  graph fitted to the stage ends up annotated in illegible four-pixel type.
   *  Dividing by the scale holds the text at one size however far out you are,
   *  which is also why it is worth gating on how big the *node* looks. */
  function drawLabel(n, r, alpha, emphasise = false) {
    const px = (v) => v / view.scale;
    ctx.globalAlpha = alpha;
    ctx.font = `${px(emphasise ? 11.5 : 10.5)}px "IBM Plex Mono", ui-monospace, monospace`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    const label = n.name.length > 34 ? n.name.slice(0, 33) + '…' : n.name;
    const y = n.y + r + px(5);
    ctx.lineWidth = px(3.5);
    ctx.strokeStyle = STAGE_BG;
    ctx.strokeText(label, n.x, y);
    ctx.fillStyle = emphasise ? '#ffffff' : '#D9E2EC';
    ctx.fillText(label, n.x, y);
    ctx.globalAlpha = 1;
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
      const over = pick(p.x, p.y);
      hovered = over ? over.id : null;
      canvas.style.cursor = over ? 'pointer' : 'grab';
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

  canvas.addEventListener('pointerleave', () => { hovered = null; });

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
      // Defaults first: re-adopting mid-unfold must not reset an edge that has
      // already drawn itself in.
      .map((r) => ({ grow: 0, revealed: false, animStart: 0, ...r }));

    // Degree, for deciding which labels are worth the room when they compete.
    // The most connected node is the one a viewer orients by — in the type
    // overview it is Document, which every other type hangs off, and which is
    // also one of the smallest circles on screen.
    for (const n of nodes) n.degree = 0;
    for (const e of edges) {
      byId.get(e.from).degree++;
      byId.get(e.to).degree++;
    }
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
    alpha = Math.max(alpha, revealed ? 0 : 0.1);
    easeCameraTo(revealed ? nodes.filter((n) => revealed.has(n.id)) : nodes);
  });

  requestAnimationFrame(frame);

  return {
    kind: 'canvas',
    setGraph(graph) {
      revealed = null; selected = null; stageOf = new Map();
      baseIds = new Set(graph.nodes.map((n) => n.id));
      adopt(graph, false);
      for (const delay of [500, 1300, 2500]) setTimeout(() => easeCameraTo(nodes), delay);
    },
    beginUnfold,
    addStage,
    /** One-shot unfold, for views that have no pipeline to follow. */
    unfold(graph) {
      beginUnfold();
      addStage({ nodes: graph.nodes, relationships: graph.relationships ?? [], stage: 1 });
    },
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
    /** Re-fit whatever the unfold is currently showing. Called when a panel
     *  resizes and changes how much of the stage is actually usable. */
    refit() {
      easeCameraTo(revealed ? nodes.filter((n) => revealed.has(n.id)) : nodes);
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
  let base = { nodes: [], relationships: [] };
  let highlighted = null;
  let selected = null;

  const toNvlNode = (n) => {
    const dim = highlighted && !highlighted.has(n.id);
    return {
      id: n.id,
      captions: [{ value: n.name }],
      caption: n.name,
      color: dim ? GHOST_FILL : (opts.colors[n.label] ?? '#8a8a8a'),
      size: n.id === selected ? 34 : 24,
      borderColor: STATUS_RING[n.status] ?? ACCENT,
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

  /** NVL runs its own layout, so a stage is just "add these and highlight the
   *  running total" — the rings arrive in order, without the radial fan. */
  function addStage({ nodes: incoming = [], relationships = [] } = {}) {
    const known = new Set(current.nodes.map((n) => n.id));
    const relIds = new Set(current.relationships.map((r) => r.id));
    current = {
      nodes: current.nodes.concat(incoming.filter((n) => !known.has(n.id))),
      relationships: current.relationships.concat(
        relationships.filter((r) => !relIds.has(r.id))),
    };
    highlighted = new Set([...(highlighted ?? []), ...incoming.map((n) => n.id)]);
    paint();
    setTimeout(() => nvl.fit([...highlighted]), 200);
  }

  return {
    kind: 'nvl',
    setGraph(graph) {
      current = graph; base = graph; highlighted = null; selected = null;
      clear(); paint();
      setTimeout(fitAll, 400);
    },
    beginUnfold() { highlighted = new Set(); },
    addStage,
    unfold(graph) {
      highlighted = new Set();
      addStage({ nodes: graph.nodes, relationships: graph.relationships ?? [] });
    },
    collapse() { current = base; highlighted = null; clear(); paint(); fitAll(); },
    setInsets() { /* NVL owns its own viewport */ },
    select(id) { selected = id; paint(); },
    focus(id) { nvl.fit([id]); },
    refit: fitAll,
    fit: fitAll,
  };
}

/* Graph renderer.
 *
 * Canvas is the default: no dependencies, instant start, full control over the
 * unfold animation. NVL is wired up behind ?renderer=nvl — it is the on-brand
 * choice but ships ESM-only, so it has to come from a CDN at runtime, which
 * costs a ~10s cold load and cannot drive the unfold.
 *
 * The unfold is staged, not one burst. /api/ask/stream sends one stage of the
 * pipeline at a time - the passages that matched, the entities in them, the
 * neighbourhood the graph adds - and each is merged into the same force layout
 * as it lands, each new node growing out of a neighbour already on screen. The
 * result is laid out the way Browser and Aura lay out a result: as a graph.
 *
 * Public surface:
 *   setGraph({nodes, relationships})       replace the graph
 *   beginUnfold()                          ghost the graph, ready for stage one
 *   addStage({nodes, relationships, stage}) reveal one more stage
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

// Labels are drawn only where they can be read. Every node labelled at once is
// the single worst thing a dense graph view does to itself: a thousand names at
// four pixels of separation is a grey texture that hides the structure it is
// annotating. So a label needs either a sparse graph, or enough zoom that the
// node is genuinely big on screen — and whatever is under the pointer or
// selected is always named, so nothing is ever unidentifiable.
const LABEL_ALWAYS_BELOW = 40;   // nodes; below this, label everything
const LABEL_MIN_ON_SCREEN = 11;  // px radius a node needs before it gets a label

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
const CAPTION_LINES = 3;      // most lines of caption a circle will hold
// Caption size follows the circle's size on screen rather than being fixed.
// A fixed size fits at one zoom and truncates every caption to four characters
// at any other — and how big the circles end up depends on the stage, the panel
// insets and how many nodes there are, none of which are known in advance.
const CAPTION_RATIO = 0.42;   // of the on-screen radius
const CAPTION_MIN_PX = 6.5;
const CAPTION_MAX_PX = 12;


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
   Canvas — force-directed, standing graph and unfolded result alike
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
  /** How many nodes are actually being looked at: the revealed set during an
   *  unfold, everything otherwise. Every size decision keys off this, so the
   *  thirty nodes of an answer are laid out and drawn as thirty nodes, not as
   *  thirty nodes standing in front of seven hundred ghosts. */
  const visibleCount = () => Math.max(1, revealed ? revealed.size : nodes.length);

  function spacing() {
    const { w, h } = size();
    const n = visibleCount();
    const area = Math.max(w * h, 1);
    const ideal = Math.max(34, Math.min(165, 0.9 * Math.sqrt(area / n)));
    // Captioned circles are much bigger than dots, so they need a floor of
    // their own: without it a fifty-node view packs radius-34 circles at a
    // spacing of seventy and they overlap. The multiplier leaves a gap of
    // roughly a circle between neighbours, which is where the relationship
    // types have to fit — pack them tighter and every type label collides with
    // a circle and is dropped.
    // 3.4 radii between centres leaves a gap of about a circle and a half,
    // which is the density Browser draws a result at: close enough to read as
    // one picture, open enough for a relationship type to sit between two
    // circles without touching either.
    return captioned() ? Math.max(ideal, CAPTION_RADIUS * 3.4) : ideal;
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
    // Gravity is what packs a layout. On a captioned result it is kept weak:
    // strong enough to hold disconnected pieces together, too weak to pull
    // nodes inside their spring length. At 0.012 the circles settled nearly
    // touching and the fit zoomed into the clump — Browser's result view has a
    // diameter or more of air between neighbours, which is where the
    // relationship types live.
    const pull = captioned() ? 0.0032 : visibleCount() > 200 ? 0.004 : 0.012;
    // Gravity is anisotropic: it pulls harder along the canvas's shorter axis.
    // A force layout settles into a disc, and a disc fitted into a wide, short
    // area is height-bound with two thirds of the width empty. Squeezing it
    // vertically in proportion to the aspect ratio gives an ellipse the shape
    // of the stage. Gentler on a captioned result, where the squeeze also
    // pushes circles into each other.
    const { w: gw, h: gh } = size();
    const aspect = Math.min(captioned() ? 1.6 : 2.4, Math.max(1, gw / Math.max(gh, 1)));
    for (const n of free) {
      n.vx -= n.x * pull;
      n.vy -= n.y * pull * aspect;
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

  // Smallest extent the fit will frame. Without a floor a one-node result is
  // zoomed to the camera's maximum and a two-node one to whatever puts their
  // centres at the viewport's edges.
  const MIN_EXTENT = 160;

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

  /** Start a fresh unfold: freeze and fade the standing graph. */
  function beginUnfold() {
    revealed = new Set();
    stageOf = new Map();
    for (const e of edges) e.revealed = false;
    for (const n of nodes) {
      // Ghosts hold still. They are the backdrop, and the layout that follows
      // is for the revealed nodes alone.
      n.pinned = true;
      n.targetAppear = GHOST_ALPHA;
      n.tx = n.ty = undefined;
      n.depth = undefined;
      n.isSeed = false;
      n.vx = n.vy = 0;
    }
    alpha = 0;
  }

  /** Reveal one more stage.
   *
   *  The revealed subgraph is laid out by the same force simulation as the
   *  standing graph — the way Browser and Aura lay out a result — rather than
   *  on a geometric fan. A fan encodes depth beautifully and reads as a
   *  diagram; a force layout encodes *connection*, which is what a graph is
   *  for, and the stages still arrive in order because each new node starts
   *  where its already-visible neighbour is and grows out of it.
   */
  function addStage({ nodes: incoming = [], relationships = [], stage = 1 } = {}) {
    if (!revealed) beginUnfold();
    mergeGraph({ nodes: incoming, relationships });

    const fresh = new Set();
    for (const n of incoming) {
      if (!byId.has(n.id) || revealed.has(n.id)) continue;
      revealed.add(n.id);
      stageOf.set(n.id, stage);
      fresh.add(n.id);
    }
    if (!revealed.size) return;

    // Where each new node should appear from: a neighbour already on screen.
    const neighbours = new Map();
    const link = (a, b) => {
      if (!neighbours.has(a)) neighbours.set(a, []);
      neighbours.get(a).push(b);
    };
    for (const e of edges) {
      if (revealed.has(e.from) && revealed.has(e.to)) { link(e.from, e.to); link(e.to, e.from); }
    }
    const settled = [...revealed].filter((id) => !fresh.has(id)).map((id) => byId.get(id));
    const centre = settled.length
      ? {
          x: settled.reduce((t, n) => t + n.x, 0) / settled.length,
          y: settled.reduce((t, n) => t + n.y, 0) / settled.length,
        }
      : { x: 0, y: 0 };

    // The layout belongs to the revealed nodes alone. Anything not revealed is
    // a ghost and holds still — asserted here, after the merge, so it cannot
    // depend on what the merge preserved.
    for (const n of nodes) {
      if (!revealed.has(n.id)) { n.pinned = true; n.targetAppear = GHOST_ALPHA; }
    }

    const now = performance.now();
    const k = spacing();
    for (const id of revealed) {
      const n = byId.get(id);
      n.pinned = false;
      n.targetAppear = 1;
      n.tx = n.ty = undefined;
      n.isSeed = stageOf.get(id) === 1;
      n.depth = (stageOf.get(id) ?? 1) - 1;
      if (!fresh.has(id)) continue;
      const anchor = (neighbours.get(id) ?? [])
        .map((other) => byId.get(other))
        .find((other) => other && !fresh.has(other.id));
      const from = anchor ?? centre;
      const angle = Math.random() * Math.PI * 2;
      const reach = k * (0.5 + 0.5 * Math.random());
      n.x = from.x + Math.cos(angle) * reach;
      n.y = from.y + Math.sin(angle) * reach;
      n.vx = n.vy = 0;
      n.appear = 0;
    }

    for (const e of edges) {
      const was = e.revealed;
      e.revealed = revealed.has(e.from) && revealed.has(e.to);
      if (e.revealed && !was) {
        e.grow = 0;
        e.animStart = now + NODE_FADE * 0.45;
      }
    }

    alpha = 1;                          // the layout runs on the revealed nodes
    for (const delay of [450, 1300, 2600]) {
      setTimeout(() => easeCameraTo(nodes.filter((n) => revealed?.has(n.id))), delay);
    }
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
  /** The segment of the straight edge from a to b that lies *between* the two
   *  circles, so the line meets each rim rather than running under the fill —
   *  which is what makes an arrowhead land on the edge of its target. */
  function edgeSpan(a, b) {
    const dx = b.x - a.x, dy = b.y - a.y;
    const d = Math.hypot(dx, dy) || 1;
    const ux = dx / d, uy = dy / d;
    const ra = radius(a), rb = radius(b);
    return {
      x0: a.x + ux * ra, y0: a.y + uy * ra,
      x1: b.x - ux * rb, y1: b.y - uy * rb,
      ux, uy, length: Math.max(0, d - ra - rb),
    };
  }

  /** Stroke the edge, truncated at t so it can draw itself in. */
  function strokeEdge(span, t) {
    ctx.beginPath();
    ctx.moveTo(span.x0, span.y0);
    ctx.lineTo(span.x0 + (span.x1 - span.x0) * t, span.y0 + (span.y1 - span.y0) * t);
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
  const captioned = () => visibleCount() <= CAPTION_LIMIT;

  /** Ghosts are the standing graph faded behind an unfold. In caption mode they
   *  are not drawn at all: Browser shows the result and nothing else, and seven
   *  hundred faint dots behind thirty captioned circles is texture, not context. */
  const isGhost = (n) => Boolean(revealed && !revealed.has(n.id));
  const ghostHidden = (n) => isGhost(n) && captioned();

  /** Shrink factor for the current graph size, 1 for anything comfortable. */
  function nodeScale() {
    const n = visibleCount();
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
    if (captioned() && !ghosted) return Math.max(explicit ?? 0, CAPTION_RADIUS);
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
      if (ghostHidden(a) || ghostHidden(b)) continue;
      const g = e.grow ?? 1;
      if (g <= 0.01) continue;
      const lit = !revealed || e.revealed;
      // An edge out of a passage is the retrieval's own work rather than a fact
      // the graph already held, so it reads warmer than the rest.
      const flow = lit && (isChunk(a) || isChunk(b));
      // Edges thin and fade as the graph grows. Eight hundred of them at the
      // weight that suits eighty overlap into a solid white mass in the middle,
      // which reads as one bright blob rather than as connections.
      const dense = visibleCount() > 200;
      const span = edgeSpan(a, b);
      if (span.length <= 0) continue;
      ctx.lineWidth = (flow ? 1.8 : lit ? (dense ? 0.85 : 1.5) : 1) / view.scale;
      ctx.strokeStyle = flow
        ? `rgba(110,231,255,${0.22 + 0.4 * g})`
        : lit
        ? `rgba(196,214,236,${(dense ? 0.05 + 0.08 * g : 0.16 + 0.26 * g)})`
        : `rgba(255,255,255,${0.05 * g})`;
      strokeEdge(span, g);

      // Arrowhead on the target's rim, the way Browser draws direction.
      if (lit && g > 0.98 && (captioned() || view.scale > 0.5)) {
        const size = captioned() ? 9 : 7;
        const tx = span.x1, ty = span.y1;
        ctx.fillStyle = flow ? 'rgba(110,231,255,0.8)' : 'rgba(196,214,236,0.6)';
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(tx - (span.ux * 0.92 - span.uy * 0.39) * size,
                   ty - (span.uy * 0.92 + span.ux * 0.39) * size);
        ctx.lineTo(tx - (span.ux * 0.92 + span.uy * 0.39) * size,
                   ty - (span.uy * 0.92 - span.ux * 0.39) * size);
        ctx.closePath();
        ctx.fill();
      }
      // The relationship type, along the relationship. Collected rather than
      // drawn: it is placed after the node captions, so a type never lands on
      // top of a node's own name.
      if (lit && g > 0.98 && (captioned() || view.scale > 1.05)) {
        let angle = Math.atan2(span.uy, span.ux);
        // Never upside down: text reads left to right whichever way the edge runs.
        if (angle > Math.PI / 2 || angle < -Math.PI / 2) angle += Math.PI;
        edgeLabels.push({
          text: e.type,
          x: (span.x0 + span.x1) / 2,
          y: (span.y0 + span.y1) / 2,
          angle,
          along: span.length,
          weight: e.properties?.count ?? 0,
          flow,
        });
      }
    }

    // nodes
    const deferredLabels = [];
    const reserved = [];
    for (const n of nodes) {
      if (ghostHidden(n)) continue;
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

  /** Relationship types, set along their edges, heaviest first, skipping any
   *  that would collide with a circle or with a type already placed.
   *
   *  Along the edge rather than horizontal at its midpoint: that is how every
   *  Neo4j surface draws a type, and it is also the only orientation in which a
   *  word can sit on a short edge between two large circles without covering
   *  one of them. A type longer than its edge is dropped rather than overlapped. */
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
      if (w > item.along - px(10)) continue;
      // Screen-space bounding box of the rotated text, for the collision test.
      const c = Math.abs(Math.cos(item.angle)), sn = Math.abs(Math.sin(item.angle));
      const bw = w * c + px(12) * sn, bh = w * sn + px(12) * c;
      const box = screenBox(item.x, item.y, bw + px(6), bh + px(4));
      if (placed.some((other) => overlaps(box, other))) continue;
      placed.push(box);
      ctx.save();
      ctx.translate(item.x, item.y);
      ctx.rotate(item.angle);
      // Stroked in the stage colour so the line does not run through the word.
      ctx.lineWidth = px(4);
      ctx.strokeStyle = STAGE_BG;
      ctx.strokeText(item.text, 0, 0);
      ctx.fillStyle = item.flow ? 'rgba(110,231,255,0.92)' : 'rgba(170,190,214,0.95)';
      ctx.fillText(item.text, 0, 0);
      ctx.restore();
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
    // A dropped node goes back into the simulation. Only ghosts stay pinned:
    // they are the frozen backdrop of an unfold, not part of its layout. This
    // used to keep revealed nodes pinned too, because the fan needed them held
    // at their targets — a force layout wants the opposite, so the graph reacts
    // to where you put a node rather than leaving a hole where it was.
    if (dragging) {
      dragging.pinned = isGhost(dragging);
      alpha = Math.max(alpha, 0.35);
    }
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
      if (ghostHidden(n)) continue;
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
        // Carried over when a node already exists. Re-adopting mid-unfold must
        // not unfreeze the ghosts or brighten them: with these reset, every
        // stage put all seven hundred background nodes back into the layout the
        // revealed ones were supposed to have to themselves.
        pinned: old?.pinned ?? false,
        appear: old?.appear ?? 0,
        targetAppear: old?.targetAppear ?? 1,
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
      // The two numbers that say whether this is a force layout right now: how
      // many nodes the simulation is moving, and how much heat it has left.
      free: nodes.filter((n) => !n.pinned).length,
      alpha: Number(alpha.toFixed(3)),
      // Mean nearest-neighbour distance among the free nodes, in node radii.
      // Around 2 the circles touch; Browser's result view sits near 3.5-4.
      spread: (() => {
        const free = nodes.filter((n) => !n.pinned);
        if (free.length < 2) return null;
        let total = 0;
        for (const a of free) {
          let best = Infinity;
          for (const b of free) {
            if (b === a) continue;
            best = Math.min(best, Math.hypot(a.x - b.x, a.y - b.y));
          }
          total += best;
        }
        const r = captioned() ? CAPTION_RADIUS : NODE_RADIUS * nodeScale();
        return Number((total / free.length / r).toFixed(2));
      })(),
      stages: [...stageOf.values()].reduce((acc, stage) => {
        acc[stage] = (acc[stage] ?? 0) + 1;
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

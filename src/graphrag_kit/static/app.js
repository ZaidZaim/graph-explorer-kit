/* Graph explorer front-end.
 *
 * NVL ships ESM-only with no UMD bundle, so it is imported from esm.sh rather
 * than bundled. If that import fails (offline, CDN blocked), renderer.js falls
 * back to a built-in canvas renderer so the demo still works.
 */

import { createRenderer } from '/static/renderer.js?v=3';

const $ = (id) => document.getElementById(id);
const api = async (path, opts) => {
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(`${path} -> ${res.status} ${await res.text()}`);
  return res.json();
};

const CHUNK_COLOR = '#7d6ea8';

/** Which ring each backend stage lands on. The order is the pipeline's own: the
 *  passages the question matched, the entities in them, and the neighbourhood
 *  the graph contributes on top. The question itself stays in the ask bar and on
 *  the answer card — it is not a thing in the graph. */
const STAGE_RING = { evidence: 1, entities: 2, neighbourhood: 3 };

const state = {
  meta: null,
  graph: { nodes: [], relationships: [] },
  activeLabels: new Set(),
  activeStatuses: new Set(),
  renderer: null,
  selected: null,
  // Nodes that exist only inside the current unfold (passages, mostly), so the
  // details panel can describe them without a round trip.
  unfoldNodes: new Map(),
};

/* ---------------- boot ---------------- */

async function boot() {
  try {
    setLoading('Reading graph metadata…');
    state.meta = await api('/api/meta');
    state.activeLabels = new Set(state.meta.labels);
    state.activeStatuses = new Set(state.meta.evidenceLevels);

    applyBranding();
    buildLabelFilters();
    buildStatusFilters();
    buildStats();
    buildRetrievers();
    buildExamples();

    setLoading('Loading the POLE graph…');
    state.renderer = await createRenderer($('graph'), {
      onNodeClick: showDetails,
      onBackgroundClick: hideDetails,
      // Chunk is not a schema label, so the project palette has no colour for
      // it — but it is a ring in every unfold.
      colors: { ...state.meta.colors, Chunk: CHUNK_COLOR },
    });

    syncInsets();
    window.addEventListener('resize', syncInsets);
    new ResizeObserver(syncInsets).observe($('answer'));
    // Dev affordance: inspect layout state from the console.
    window.__graphrag = { state, renderer: state.renderer };
    await refreshGraph();
    setLoading(null);
  } catch (err) {
    console.error(err);
    setLoading(`Failed to start: ${err.message}`);
  }
  wireEvents();
}

/** Title, subtitle and seed questions come from the active project, so the
 *  engine ships no branding of its own. */
function applyBranding() {
  document.title = `${state.meta.title} — Knowledge Graph`;
  $('brand-title').textContent = state.meta.title;
  $('brand-subtitle').textContent = state.meta.subtitle;
  const first = state.meta.examples?.[0];
  if (first) $('question').placeholder = `Ask the graph — e.g. ${first.toLowerCase()}`;
}

/** Tell the renderer which parts of the stage are covered by floating panels,
 *  so fitting the graph does not centre it under the answer card. */
function syncInsets() {
  const stage = $('stage').getBoundingClientRect();
  const answer = $('answer');
  const askBar = $('ask-bar');
  let left = 0, top = 0;
  if (!answer.hidden) {
    const r = answer.getBoundingClientRect();
    // Below the narrow breakpoint the card spans the whole stage. Reserving its
    // width there leaves a sliver and shoves the graph off the right edge, so
    // reserve its height instead.
    if (r.width > stage.width * 0.6) top = Math.max(0, r.bottom - stage.top + 16);
    else left = Math.max(0, r.right - stage.left + 16);
  }
  const bottom = askBar ? stage.bottom - askBar.getBoundingClientRect().top + 16 : 0;
  state.renderer?.setInsets({ left, top, bottom: Math.max(0, bottom) });
  refitSoon();
}

// The answer card grows as stages and then prose arrive, which moves the insets
// under the graph. Re-fit once the churn settles rather than on every pixel.
let refitTimer = null;
function refitSoon() {
  clearTimeout(refitTimer);
  refitTimer = setTimeout(() => state.renderer?.refit(), 160);
}

function setLoading(text) {
  const el = $('loading');
  if (!text) { el.hidden = true; return; }
  el.hidden = false;
  $('loading-text').textContent = text;
}

/* ---------------- sidebar ---------------- */

function buildLabelFilters() {
  const ul = $('label-filters');
  ul.innerHTML = '';
  for (const label of state.meta.labels) {
    const color = state.meta.colors[label];
    const li = document.createElement('li');
    li.style.color = color;
    li.innerHTML =
      `<span class="swatch" style="background:${color}"></span>` +
      `<span style="color:var(--text)">${label}</span>` +
      `<span class="count">${state.meta.counts[label] ?? 0}</span>`;
    li.onclick = () => {
      state.activeLabels.has(label)
        ? state.activeLabels.delete(label)
        : state.activeLabels.add(label);
      li.classList.toggle('off', !state.activeLabels.has(label));
      refreshGraph();
    };
    ul.appendChild(li);
  }
}

// Evidence levels are ordered strongest-first by the project; the palette maps
// onto that order rather than onto specific level names.
const EVIDENCE_SWATCHES = ['var(--confirmed)', 'var(--reported)', 'var(--rumored)'];
const statusColor = (i) => EVIDENCE_SWATCHES[Math.min(i, EVIDENCE_SWATCHES.length - 1)];

function buildStatusFilters() {
  const ul = $('status-filters');
  ul.innerHTML = '';
  state.meta.evidenceLevels.forEach((status, i) => {
    const li = document.createElement('li');
    li.style.color = statusColor(i);
    li.innerHTML =
      `<span class="swatch" style="background:${statusColor(i)}"></span>` +
      `<span style="color:var(--text)">${status}</span>` +
      `<span class="count">${state.meta.statuses[status] ?? 0}</span>`;
    li.onclick = () => {
      state.activeStatuses.has(status)
        ? state.activeStatuses.delete(status)
        : state.activeStatuses.add(status);
      li.classList.toggle('off', !state.activeStatuses.has(status));
      refreshGraph();
    };
    ul.appendChild(li);
  });
}

function buildStats() {
  const dl = $('stats');
  const rows = [
    ['Documents', state.meta.documents],
    ['Chunks', state.meta.chunks],
    ['Entities', Object.values(state.meta.counts).reduce((a, b) => a + b, 0)],
    ['Relationships', state.meta.relationships],
  ];
  dl.innerHTML = rows.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('');
}

function buildRetrievers() {
  const sel = $('retriever');
  sel.innerHTML = state.meta.retrievers
    .map((r) => `<option value="${r}"${r === 'hybrid-cypher' ? ' selected' : ''}>${r}</option>`)
    .join('');
}

function buildExamples() {
  const box = $('examples');
  box.innerHTML = '';
  for (const q of state.meta.examples ?? []) {
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = q;
    b.onclick = () => { $('question').value = q; askQuestion(); };
    box.appendChild(b);
  }
}

/* ---------------- graph ---------------- */

async function refreshGraph() {
  const labels = [...state.activeLabels].join(',');
  const status = [...state.activeStatuses].join(',');
  if (!labels || !status) {
    state.graph = { nodes: [], relationships: [] };
    state.renderer.setGraph(state.graph);
    $('graph-empty').hidden = false;
    return;
  }
  state.graph = await api(`/api/graph?labels=${encodeURIComponent(labels)}&status=${encodeURIComponent(status)}`);
  $('graph-empty').hidden = state.graph.nodes.length > 0;
  state.renderer.setGraph(state.graph);
}

/* ---------------- details ---------------- */

async function showDetails(nodeId) {
  const node = state.graph.nodes.find((n) => n.id === nodeId)
    ?? state.unfoldNodes.get(nodeId)
    ?? (await api(`/api/expand?id=${encodeURIComponent(nodeId)}`)).nodes.find((n) => n.id === nodeId);
  if (!node) return;

  if (node.label === 'Chunk') { showChunkDetails(node); return; }

  state.selected = nodeId;
  const color = state.meta.colors[node.label] ?? '#888';
  $('detail-label').textContent = node.label ?? 'Entity';
  $('detail-label').style.background = color;
  $('detail-name').textContent = node.name;

  const ev = $('detail-status');
  ev.textContent = node.evidence_levels?.length > 1
    ? `${node.status} — also seen as ${node.evidence_levels.filter((s) => s !== node.status).join(', ')}`
    : node.status;
  ev.className = `evidence ${node.status}`;

  $('detail-description').textContent = node.description ?? '';

  const props = [
    ['Role', node.role], ['Kind', node.kind], ['Date', node.date],
    ['Inspiration', node.inspiration],
    ['Fictional', node.fictional === null || node.fictional === undefined ? null : String(node.fictional)],
  ].filter(([, v]) => v);
  $('detail-props').innerHTML = props.map(([k, v]) => `<dt>${k}</dt><dd>${escapeHtml(v)}</dd>`).join('');

  const sub = await api(`/api/expand?id=${encodeURIComponent(nodeId)}`);
  const byId = new Map(sub.nodes.map((n) => [n.id, n]));
  const ul = $('detail-rels');
  ul.innerHTML = '';
  for (const rel of sub.relationships) {
    const outgoing = rel.from === nodeId;
    const other = byId.get(outgoing ? rel.to : rel.from);
    if (!other) continue;
    const li = document.createElement('li');
    li.innerHTML =
      `<span class="rel-type">${outgoing ? '→' : '←'} ${rel.type}</span>` +
      `<span class="dir">${escapeHtml(other.label ?? '')}:</span> ${escapeHtml(other.name)}`;
    li.onclick = () => { state.renderer.focus(other.id); showDetails(other.id); };
    ul.appendChild(li);
  }
  if (!ul.children.length) ul.innerHTML = '<li style="cursor:default">No connections in the graph.</li>';

  $('details').hidden = false;
  $('app').classList.add('with-details');
  state.renderer.select(nodeId);
}

/** A retrieved passage is raw source text, not a graph record — it has no
 *  evidence level and no relationships of its own worth listing. */
function showChunkDetails(node) {
  state.selected = node.id;
  $('detail-label').textContent = 'Passage';
  $('detail-label').style.background = CHUNK_COLOR;
  $('detail-name').textContent = node.source ?? 'Retrieved passage';
  $('detail-status').textContent = 'retrieved for this question';
  $('detail-status').className = 'evidence';
  $('detail-description').textContent = node.text ?? node.description ?? '';
  $('detail-props').innerHTML = node.score
    ? `<dt>Score</dt><dd>${node.score.toFixed(3)}</dd>`
    : '';
  $('detail-rels').innerHTML =
    '<li style="cursor:default">The entities extracted from this passage are the next ring out.</li>';
  $('details').hidden = false;
  $('app').classList.add('with-details');
  state.renderer.select(node.id);
}

function hideDetails() {
  state.selected = null;
  $('details').hidden = true;
  $('app').classList.remove('with-details');
  state.renderer?.select(null);
}

/* ---------------- ask ---------------- */

/** Read a text/event-stream response, calling back once per complete event.
 *  EventSource cannot POST, so the stream is read off fetch by hand. */
async function streamEvents(path, body, onEvent) {
  const res = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`${path} -> ${res.status} ${await res.text()}`);

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let split;
    while ((split = buffer.indexOf('\n\n')) >= 0) {
      const raw = buffer.slice(0, split);
      buffer = buffer.slice(split + 2);
      let name = 'message', data = '';
      for (const line of raw.split('\n')) {
        if (line.startsWith('event:')) name = line.slice(6).trim();
        else if (line.startsWith('data:')) data += line.slice(5).trim();
      }
      if (data) onEvent(name, JSON.parse(data));
    }
  }
}

/** Stages arrive as fast as the database answers, which is faster than the eye
 *  can follow. This holds each one on screen long enough to be read. */
function beatQueue(gap) {
  const pending = [];
  let running = false;
  const pump = async () => {
    if (running) return;
    running = true;
    while (pending.length) {
      pending.shift()();
      await new Promise((r) => setTimeout(r, gap));
    }
    running = false;
  };
  return { push(fn) { pending.push(fn); pump(); } };
}

function setStage(text) {
  const el = $('answer-stage');
  el.textContent = text ?? '';
  el.hidden = !text;
}

async function askQuestion() {
  const question = $('question').value.trim();
  if (!question) return;

  const btn = $('ask-button');
  btn.disabled = true;
  btn.textContent = 'Thinking…';
  $('answer').hidden = false;
  syncInsets();
  $('answer-body').innerHTML = '';
  $('answer-context').innerHTML = '';
  setStage('Sending the question…');

  // Ghost the standing graph and wait for stage one. Each stage adds a ring, so
  // the picture grows in the order the answer was reasoned out instead of
  // arriving all at once at the end.
  state.unfoldNodes = new Map();
  state.renderer.beginUnfold();

  const beat = beatQueue(640);
  let answered = false;
  let gotRings = false;

  try {
    await streamEvents('/api/ask/stream',
      { question, retriever: $('retriever').value, top_k: 5 },
      (name, data) => {
        if (name === 'stage') {
          beat.push(() => setStage(data.label));
        } else if (name === 'unfold') {
          gotRings = true;
          beat.push(() => {
            setStage(data.label);
            for (const n of data.nodes) state.unfoldNodes.set(n.id, n);
            state.renderer.addStage({
              nodes: data.nodes,
              relationships: data.relationships ?? [],
              stage: STAGE_RING[data.stage] ?? 1,
            });
          });
        } else if (name === 'answer') {
          answered = true;
          setStage(null);
          $('answer-body').innerHTML = markEvidence(renderMarkdown(data.answer));
          $('answer-context').innerHTML = data.context.length
            ? data.context.map((c) => `<pre>${escapeHtml(c)}</pre>`).join('')
            : '<pre>(no context returned)</pre>';
        } else if (name === 'warning') {
          console.warn(data.message);
        } else if (name === 'error') {
          throw new Error(data.message);
        }
      });
    if (!answered) throw new Error('the stream ended before the answer arrived');
  } catch (err) {
    console.error(err);
    setStage(null);
    // A request that produced no rings at all leaves the graph ghosted with
    // nothing to look at. Put it back rather than stranding the viewer.
    if (!gotRings) {
      state.unfoldNodes = new Map();
      state.renderer.collapse();
    }
    // fetch rejects with a TypeError when it cannot reach the host at all,
    // which as "Failed to fetch" reads like a bug in the page.
    $('answer-body').textContent = err.name === 'TypeError'
      ? 'Could not reach the server — is it still running?'
      : `Request failed: ${err.message}`;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Ask';
  }
}

/** Minimal markdown -> HTML. Models emit **bold**, `code` and bullet lists
 *  whether or not you ask for prose; rendering literal asterisks looks broken.
 *  Escapes first, so this never introduces markup from model output. */
function renderMarkdown(text) {
  const lines = escapeHtml(text).split('\n');
  const out = [];
  let inList = false;
  for (const raw of lines) {
    const line = raw.trimEnd();
    const bullet = line.match(/^\s*[-*]\s+(.*)$/);
    if (bullet) {
      if (!inList) { out.push('<ul>'); inList = true; }
      out.push(`<li>${inline(bullet[1])}</li>`);
      continue;
    }
    if (inList) { out.push('</ul>'); inList = false; }
    if (!line.trim()) { out.push('<p class="gap"></p>'); continue; }
    out.push(`<p>${inline(line)}</p>`);
  }
  if (inList) out.push('</ul>');
  return out.join('');
}

function inline(s) {
  return s
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*]+)\*/g, '$1<em>$2</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
}

/** Colour the evidence words the model is instructed to emit. */
function markEvidence(html) {
  return html.replace(/\[?\b(confirmed|reported|rumou?red)\b\]?/gi, (m) => {
    const key = /rumou?red/i.test(m) ? 'rumored' : m.replace(/[[\]]/g, '').toLowerCase();
    return `<span class="ev ev-${key}">${m}</span>`;
  });
}

/* ---------------- search ---------------- */

let searchTimer = null;
async function onSearch() {
  clearTimeout(searchTimer);
  const q = $('search').value.trim();
  const list = $('search-results');
  if (!q) { list.hidden = true; return; }
  searchTimer = setTimeout(async () => {
    try {
      const res = await api(`/api/search?q=${encodeURIComponent(q)}`);
      list.innerHTML = '';
      for (const n of res.nodes) {
        const li = document.createElement('li');
        li.innerHTML =
          `<span class="swatch" style="width:9px;height:9px;border-radius:3px;background:${state.meta.colors[n.label] ?? '#888'}"></span>` +
          `${escapeHtml(n.name)}`;
        li.onclick = () => {
          list.hidden = true;
          $('search').value = '';
          state.renderer.focus(n.id);
          showDetails(n.id);
        };
        list.appendChild(li);
      }
      list.hidden = res.nodes.length === 0;
    } catch (err) { console.error(err); }
  }, 180);
}

/* ---------------- misc ---------------- */

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

async function showTimeline() {
  const res = await api('/api/timeline');
  state.renderer.unfold({ nodes: res.nodes, relationships: [] });
  $('answer').hidden = false;
  syncInsets();
  setStage(null);
  $('answer-body').innerHTML = res.nodes
    .map((n) => `<strong>${escapeHtml(n.date)}</strong>  ${escapeHtml(n.name)}`)
    .join('\n');
  $('answer-context').innerHTML = '';
}

function wireEvents() {
  $('ask-form').addEventListener('submit', (e) => { e.preventDefault(); askQuestion(); });
  $('search').addEventListener('input', onSearch);
  $('close-details').addEventListener('click', hideDetails);
  $('close-answer').addEventListener('click', () => {
    $('answer').hidden = true;
    syncInsets();
    setStage(null);
    state.unfoldNodes = new Map();
    state.renderer?.collapse();
  });
  $('reset-view').addEventListener('click', async () => {
    $('answer').hidden = true;
    syncInsets();
    setStage(null);
    state.unfoldNodes = new Map();
    await refreshGraph();
  });
  $('show-timeline').addEventListener('click', showTimeline);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { hideDetails(); $('search-results').hidden = true; }
  });
}

boot();

/* Graph explorer front-end.
 *
 * Three views over one graph:
 *   graph     the records themselves, filtered by POLE group and label
 *   schema    the model — node types, their properties, and what may link to
 *             what — sized by how many instances the graph actually holds
 *   timeline  the dated events, in order
 *
 * Asking a question streams the pipeline's stages (see /api/ask/stream) and the
 * graph unfolds one ring per stage, so the picture grows in the order the answer
 * was reasoned out. Adding a document streams the same way: the file is chunked,
 * embedded and extracted against the same schema, and what it added lights up.
 *
 * NVL ships ESM-only with no UMD bundle, so it is imported from esm.sh rather
 * than bundled. If that import fails (offline, CDN blocked), renderer.js falls
 * back to a built-in canvas renderer so the demo still works.
 */

import { createRenderer } from '/static/renderer.js?v=5';

const $ = (id) => document.getElementById(id);
const api = async (path, opts) => {
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(`${path} -> ${res.status} ${await res.text()}`);
  return res.json();
};

const CHUNK_COLOR = '#41506B';

/* ---------------- theme ---------------- */

const THEME_KEY = 'graphrag-theme';

/** The theme the page is showing. index.html sets it before first paint from
 *  the stored choice or the OS preference, so this is never undefined. */
const currentTheme = () => (document.documentElement.dataset.theme === 'light' ? 'light' : 'dark');

/** Switch the whole surface: the CSS tokens flip on `data-theme`, and the
 *  canvas re-reads them. `persist` is false when following the OS rather
 *  than the reader's own click, so a later OS change is still honoured. */
function applyTheme(theme, { persist = true } = {}) {
  document.documentElement.dataset.theme = theme;
  const toggle = $('theme-toggle');
  toggle.setAttribute('aria-checked', String(theme === 'light'));
  toggle.setAttribute('aria-label', theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode');
  if (persist) {
    try { localStorage.setItem(THEME_KEY, theme); } catch { /* storage blocked */ }
  }
  state.renderer?.setTheme?.();
}

function wireTheme() {
  applyTheme(currentTheme(), { persist: false });
  $('theme-toggle').addEventListener('click', () =>
    applyTheme(currentTheme() === 'light' ? 'dark' : 'light'));
  // Follow the OS only while the reader has not chosen for themselves.
  matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
    let stored = null;
    try { stored = localStorage.getItem(THEME_KEY); } catch { /* storage blocked */ }
    if (!stored) applyTheme(e.matches ? 'light' : 'dark', { persist: false });
  });
}

/** Which ring each backend stage lands on. The order is the pipeline's own: the
 *  passages the question matched, the entities in them, and the neighbourhood
 *  the graph contributes on top. The question itself stays in the ask bar and on
 *  the answer card — it is not a thing in the graph. */
const STAGE_RING = { evidence: 1, entities: 2, neighbourhood: 3 };

/** Segments in the pipeline indicator. Four is the number of stages a
 *  hybrid-cypher answer actually goes through; the agent decides its own route
 *  and simply fills them as it goes. */
const PROGRESS_STEPS = 4;

/** Node radius from a count, for the views that draw one node per type. Area,
 *  not radius, tracks the count — a linear radius makes 261 Observations look
 *  thirty times more important than 1 Redaction rather than sixteen, and swamps
 *  the small types entirely. */
const typeRadius = (count, max) => 11 + 26 * Math.sqrt(count / Math.max(max, 1));

const CAPTIONS = {
  graph: 'One node per record type, sized by how many records carry it. Click a type to open its records.',
  graphAll: 'Every extracted record. Zoom in for names, or hover a node.',
  graphType: 'The most connected records of one type, with what they link to. Click one to open it.',
  graphRecord: 'One record and everything it links to, with each relationship named.',
  schema: 'The POLE model this corpus is held to. Node size is how many records carry that type.',
  timeline: 'Events carrying a date, earliest first. Dates are as precise as the document allowed.',
};

const state = {
  meta: null,
  graph: { nodes: [], relationships: [] },
  schema: null,
  view: 'graph',
  // 'all' draws every record, 'overview' one node per type, and 'type' /
  // 'record' are the drill-downs from the overview. The graph opens on the
  // records: one node per type is what the Schema tab already shows, and the
  // Graph tab should be the graph.
  graphMode: 'all',
  drilledInto: null,
  focused: null,
  activeLabels: new Set(),
  activeStatuses: new Set(),
  // Entities with no relationship at all. A third of this corpus, and as a
  // default view they bury the structure, so they are opt-in.
  showIsolated: false,
  renderer: null,
  selected: null,
  // Nodes that exist only inside the current unfold (passages, mostly), so the
  // details panel can describe them without a round trip.
  unfoldNodes: new Map(),
  newIds: new Set(),
};

/* ---------------- boot ---------------- */

async function boot() {
  wireTheme();
  try {
    setLoading('Reading graph metadata…');
    state.meta = await api('/api/meta');
    state.activeLabels = new Set(state.meta.labels);
    state.activeStatuses = new Set(state.meta.evidenceLevels);

    applyBranding();
    buildPoleFilters();
    buildStatusFilters();
    buildStats();
    buildRetrievers();
    buildExamples();
    startClock();
    loadSources();

    setLoading('Loading the graph…');
    state.renderer = await createRenderer($('graph'), {
      onNodeClick: showDetails,
      onBackgroundClick: hideDetails,
      // Chunk is not a schema label, so the project palette has no colour for
      // it — but it is a ring in every unfold.
      colors: { ...state.meta.colors, Chunk: CHUNK_COLOR },
    });

    syncInsets();
    window.addEventListener('resize', syncInsets);
    // The graph area changes size whenever the dock does - an answer arriving,
    // or closing - with no window resize to hear about it.
    new ResizeObserver(syncInsets).observe($('graph-area'));
    new ResizeObserver(syncInsets).observe($('details'));
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
  if (first) $('question').placeholder = `Ask the record — e.g. ${first.toLowerCase()}`;
  $('evidence-panel').hidden = !state.meta.gradesEvidence;
  $('views').querySelector('[data-view="timeline"]').hidden = !state.meta.hasTimeline;
  $('isolated-count').textContent = state.meta.isolated ?? 0;
  const suffixes = state.meta.uploadSuffixes ?? [];
  if (suffixes.length) $('upload-hint').textContent = `Drop a file (${suffixes.join(' ')})`;
  updateHud();
}

function updateHud() {
  const entities = Object.values(state.meta.counts).reduce((a, b) => a + b, 0);
  $('hud-records').textContent = entities.toLocaleString();
  $('hud-links').textContent = state.meta.relationships.toLocaleString();
  $('hud-docs').textContent = state.meta.documents;
}

/** The source site keeps a clock in its masthead; this is the same idea and the
 *  same purpose — it says the page is live rather than a screenshot. */
function startClock() {
  const tick = () => {
    $('hud-clock').textContent = new Date().toISOString().slice(11, 19);
  };
  tick();
  setInterval(tick, 1000);
}

/** Tell the renderer which parts of the graph area are covered by a floating
 *  panel, so fitting the graph does not centre it underneath one.
 *
 *  Little is covered now that the answer lives in the dock and the dock is in
 *  the layout flow rather than over the canvas. The one case left is the record
 *  detail panel, which becomes a fixed overlay on the right below 1240px. */
function syncInsets() {
  const area = $('graph-area').getBoundingClientRect();
  const details = $('details');
  let right = 0;
  if (!details.hidden) {
    const r = details.getBoundingClientRect();
    // Overlapping the graph area means it is the fixed overlay, not a column.
    if (r.left < area.right) right = Math.max(0, area.right - r.left);
  }
  state.renderer?.setInsets({ left: 0, top: 0, right, bottom: 0 });
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

function setCaption(text) {
  const el = $('stage-caption');
  el.textContent = text ?? '';
  el.hidden = !text;
}

function setNote(text) {
  const el = $('stage-note');
  el.textContent = text ?? '';
  el.hidden = !text;
}

/* ---------------- POLE filters ---------------- */

function buildPoleFilters() {
  const box = $('pole-groups');
  box.innerHTML = '';
  const { groupColors, colors, counts } = state.meta;
  // A project need not declare groups. Without a fallback the whole filter list
  // would simply be absent for one that does not, since there would be no group
  // to hang the labels off — so the labels become one unnamed group.
  const grouped = Object.keys(state.meta.groups ?? {}).length > 0;
  const groups = grouped ? state.meta.groups : { '': state.meta.labels };
  $('pole-panel').querySelector('h2').firstChild.textContent =
    grouped ? 'POLE ' : 'Entities ';

  for (const [group, labels] of Object.entries(groups)) {
    const total = labels.reduce((sum, l) => sum + (counts[l] ?? 0), 0);
    const div = document.createElement('div');
    div.className = 'pole-group';
    div.style.setProperty('--swatch', groupColors[group] ?? 'var(--muted)');

    const head = document.createElement('div');
    head.className = 'pole-head';
    head.innerHTML = `<span>${group}</span><span class="count">${total}</span>`;
    head.hidden = !group;
    // Clicking a group toggles all of its labels at once: the group *is* the
    // POLE class, and "show me only the people" is the question being asked.
    head.onclick = () => {
      const anyOn = labels.some((l) => state.activeLabels.has(l));
      for (const l of labels) {
        if (anyOn) state.activeLabels.delete(l);
        else state.activeLabels.add(l);
      }
      syncFilterUi();
      refreshGraph();
    };
    div.appendChild(head);

    const ul = document.createElement('ul');
    ul.className = 'pole-labels';
    for (const label of labels) {
      const li = document.createElement('li');
      li.dataset.label = label;
      li.style.setProperty('--swatch', colors[label] ?? groupColors[group]);
      li.innerHTML =
        `<span class="dot"></span><span class="l-name">${label}</span>` +
        `<span class="count">${counts[label] ?? 0}</span>`;
      li.onclick = (e) => {
        e.stopPropagation();
        state.activeLabels.has(label)
          ? state.activeLabels.delete(label)
          : state.activeLabels.add(label);
        syncFilterUi();
        refreshGraph();
      };
      ul.appendChild(li);
    }
    div.appendChild(ul);
    box.appendChild(div);
  }
  syncFilterUi();
}

function syncFilterUi() {
  for (const li of document.querySelectorAll('.pole-labels li')) {
    li.classList.toggle('is-off', !state.activeLabels.has(li.dataset.label));
  }
  for (const [group, labels] of Object.entries(state.meta.groups ?? {})) {
    const div = [...document.querySelectorAll('.pole-group')].find(
      (d) => d.querySelector('.pole-head span').textContent === group);
    div?.classList.toggle('is-off', !labels.some((l) => state.activeLabels.has(l)));
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
      `<span class="dot" style="background:${statusColor(i)}"></span>` +
      `<span style="color:var(--text)">${status}</span>` +
      `<span class="count">${state.meta.statuses[status] ?? 0}</span>`;
    li.onclick = () => {
      state.activeStatuses.has(status)
        ? state.activeStatuses.delete(status)
        : state.activeStatuses.add(status);
      li.classList.toggle('is-off', !state.activeStatuses.has(status));
      refreshGraph();
    };
    ul.appendChild(li);
  });
}

function buildStats() {
  const entities = Object.values(state.meta.counts).reduce((a, b) => a + b, 0);
  $('stats').innerHTML = [
    ['Records', entities.toLocaleString()],
    ['Links', state.meta.relationships.toLocaleString()],
    ['Documents', state.meta.documents],
    ['Passages', state.meta.chunks],
  ].map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('');
}

async function loadSources() {
  try {
    const { sources } = await api('/api/documents');
    $('sources').innerHTML = sources.map((s) =>
      `<li${state.newIds.has(s.id) ? ' class="is-new"' : ''}>${escapeHtml(s.name)}` +
      `<br><span class="meta">${s.chunks} passages · ${s.entities} records</span></li>`
    ).join('');
  } catch (err) {
    console.error(err);
  }
}

function buildRetrievers() {
  $('retriever').innerHTML = state.meta.retrievers
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

/* ---------------- views ---------------- */

async function setView(view) {
  state.view = view;
  for (const tab of document.querySelectorAll('.view-tab')) {
    tab.classList.toggle('is-active', tab.dataset.view === view);
  }
  $('pole-panel').hidden = view !== 'graph';
  if (view === 'graph') syncModeUi();
  hideDetails();
  closeAnswer();
  setCaption(CAPTIONS[view]);
  if (view !== 'graph') setNote(null);

  if (view === 'graph') return refreshGraph();
  if (view === 'schema') return showSchema();
  if (view === 'timeline') return showTimeline();
}

async function refreshGraph() {
  if (state.view !== 'graph') return;
  const labels = [...state.activeLabels].join(',');
  const status = [...state.activeStatuses].join(',');
  if (!labels || (state.meta.gradesEvidence && !status)) {
    state.graph = { nodes: [], relationships: [] };
    state.renderer.setGraph(state.graph);
    $('graph-empty').hidden = false;
    return;
  }

  if (state.graphMode === 'overview') {
    const data = await api(`/api/overview?labels=${encodeURIComponent(labels)}`);
    const max = Math.max(1, ...data.nodes.map((n) => n.count));
    state.graph = {
      nodes: data.nodes.map((n) => ({ ...n, radius: typeRadius(n.count, max) })),
      relationships: data.relationships,
    };
    setNote('Click a type to open its records');
  } else if (state.graphMode === 'record' && state.focused) {
    const data = await api(`/api/expand?id=${encodeURIComponent(state.focused)}`);
    state.graph = { nodes: data.nodes, relationships: data.relationships };
    const node = data.nodes.find((n) => n.id === state.focused);
    setNote(`${node?.label ?? 'Record'}: ${data.nodes.length - 1} direct connections`);
  } else if (state.graphMode === 'type' && state.drilledInto) {
    const data = await api(`/api/instances?label=${encodeURIComponent(state.drilledInto)}`);
    state.graph = { nodes: data.nodes, relationships: data.relationships };
    setNote(data.shown < data.total
      ? `${state.drilledInto}: ${data.shown} of ${data.total} records, most connected first`
      : `${state.drilledInto}: all ${data.total} records`);
  } else {
    state.graph = await api(
      `/api/graph?labels=${encodeURIComponent(labels)}&status=${encodeURIComponent(status)}` +
      `&connected=${state.showIsolated ? 'false' : 'true'}`);
    setNote(state.showIsolated || !state.meta.isolated
      ? null
      : `${state.meta.isolated} unlinked records hidden`);
  }

  $('graph-empty').hidden = state.graph.nodes.length > 0;
  state.renderer.setGraph(state.graph);
  setCaption(CAPTIONS[
    { overview: 'graph', type: 'graphType', all: 'graphAll', record: 'graphRecord' }[
      state.graphMode]]);
  syncModeUi();
}

function syncModeUi() {
  // Unlinked records are only a thing the records view can show or hide; in the
  // overview they are already counted inside their type.
  $('structure-filters').hidden = state.graphMode !== 'all';
  for (const b of document.querySelectorAll('#graph-mode button')) {
    // The drill-down is a state of the overview, so the Types button stays lit.
    const active = b.dataset.mode === (state.graphMode === 'all' ? 'all' : 'overview');
    b.classList.toggle('is-active', active);
  }
}

async function setGraphMode(mode) {
  state.graphMode = mode;
  state.drilledInto = null;
  state.focused = null;
  if (state.view !== 'graph') { await setView('graph'); return; }
  await refreshGraph();
}

/** Open one type's records from the overview. */
async function drillInto(label) {
  state.graphMode = 'type';
  state.drilledInto = label;
  state.focused = null;
  hideDetails();
  await refreshGraph();
}

/** Open one record: itself, its neighbours, and every relationship named.
 *
 *  The third level of the same idea — types, then a type's records, then one
 *  record — and the only one small enough that every circle carries its caption
 *  and every edge carries its type. This is how a graph is meant to be read.
 */
async function focusRecord(id) {
  state.graphMode = 'record';
  state.focused = id;
  await refreshGraph();
  state.renderer.select(id);
}

/** The schema as a graph: one node per type, sized by how many records carry it,
 *  and one edge per pattern the schema licenses. */
async function showSchema() {
  if (!state.schema) state.schema = await api('/api/schema');
  const max = Math.max(1, ...state.schema.nodes.map((n) => n.count));
  const nodes = state.schema.nodes.map((n) => ({
    ...n,
    radius: typeRadius(n.count, max),
    name: `${n.label} (${n.count})`,
  }));
  state.graph = { nodes, relationships: state.schema.relationships };
  $('graph-empty').hidden = true;
  state.renderer.setGraph(state.graph);
}

async function showTimeline() {
  const res = await api('/api/timeline');
  state.renderer.unfold({ nodes: res.nodes, relationships: [] });
  for (const n of res.nodes) state.unfoldNodes.set(n.id, n);
  $('answer').hidden = false;
  $('examples').hidden = true;
  $('answer-title').textContent = `Timeline · ${res.nodes.length} dated events`;
  $('progress').hidden = true;
  $('answer-body').className = 'log';
  $('answer-body').innerHTML = res.nodes.map((n) =>
    `<div class="log-row" data-id="${escapeHtml(n.id)}">` +
    `<span class="log-date">${escapeHtml(shortDate(n.date))}</span>` +
    `<span class="log-name">${escapeHtml(n.name)}</span></div>`
  ).join('') || '<p>No dated events in the graph.</p>';
  $('answer-context').innerHTML = '';
  $('context-details').hidden = true;
  for (const row of $('answer-body').querySelectorAll('.log-row')) {
    row.onclick = () => { state.renderer.focus(row.dataset.id); showDetails(row.dataset.id); };
  }
  syncInsets();
}

/** Dates in this corpus range from a bare year to a full ISO timestamp. Show
 *  the day where there is one and no more — a fabricated 00:00:00 reads as
 *  precision the document never had. */
function shortDate(value) {
  const text = String(value ?? '');
  const iso = text.match(/^(\d{4})(-\d{2})?(-\d{2})?/);
  return iso ? iso[0] : text.slice(0, 12);
}

/* ---------------- details ---------------- */

async function showDetails(nodeId) {
  if (state.view === 'schema') return showSchemaDetails(nodeId);
  // In the overview a node *is* a type, so clicking it opens the type rather
  // than describing a record that does not exist.
  if (state.view === 'graph' && state.graphMode === 'overview') return drillInto(nodeId);

  const node = state.graph.nodes.find((n) => n.id === nodeId)
    ?? state.unfoldNodes.get(nodeId)
    ?? (await api(`/api/expand?id=${encodeURIComponent(nodeId)}`)).nodes.find((n) => n.id === nodeId);
  if (!node) return;

  if (node.label === 'Chunk') { showChunkDetails(node); return; }

  const unfolding = !$('answer').hidden;
  if (state.view === 'graph' && !unfolding && state.focused !== nodeId) {
    focusRecord(nodeId);
  }

  state.selected = nodeId;
  openDetails(node.label, state.meta.colors[node.label] ?? '#8894a8');
  $('detail-group').textContent = node.group ? `POLE · ${node.group}` : '';
  $('detail-name').textContent = node.name;

  const ev = $('detail-status');
  ev.hidden = !node.status;
  if (node.status) {
    ev.textContent = node.evidence_levels?.length > 1
      ? `${node.status} — also seen as ${node.evidence_levels.filter((s) => s !== node.status).join(', ')}`
      : node.status;
    ev.className = `evidence ${node.status}`;
  }

  $('detail-description').textContent = node.description ?? '';
  $('detail-props').innerHTML = propertyRows(node);

  const sub = await api(`/api/expand?id=${encodeURIComponent(nodeId)}`);
  const byId = new Map(sub.nodes.map((n) => [n.id, n]));
  const ul = $('detail-rels');
  ul.innerHTML = '';
  for (const rel of sub.relationships) {
    if (rel.from !== nodeId && rel.to !== nodeId) continue;
    const outgoing = rel.from === nodeId;
    const other = byId.get(outgoing ? rel.to : rel.from);
    if (!other) continue;
    const li = document.createElement('li');
    li.innerHTML =
      `<span class="rel-type">${outgoing ? '→' : '←'} ${rel.type}</span>` +
      `<span class="dir">${escapeHtml(other.label ?? '')}</span> ${escapeHtml(other.name)}`;
    li.onclick = () => { state.renderer.focus(other.id); showDetails(other.id); };
    ul.appendChild(li);
  }
  if (!ul.children.length) {
    ul.innerHTML = '<li class="inert">No connections in the graph.</li>';
  }
  state.renderer.select(nodeId);
}

/** Properties, minus the ones already shown above as name or description.
 *  Everything else the extractor recorded is shown as-is: in this corpus the
 *  measurements *are* the record. */
function propertyRows(node) {
  const shown = new Set(['description', 'evidence_levels']);
  const nameProps = ['name', 'title', 'text', 'filename', 'number', 'reason'];
  // Only the property that actually produced the display name is redundant.
  for (const key of nameProps) {
    if (node.properties?.[key] && String(node.properties[key]).startsWith(node.name.slice(0, 40))) {
      shown.add(key);
      break;
    }
  }
  const rows = Object.entries(node.properties ?? {})
    .filter(([k, v]) => !shown.has(k) && v !== null && v !== '')
    .map(([k, v]) => {
      const value = Array.isArray(v) ? v.join(', ') : String(v);
      const redacted = /\[REDACTED\]|\[ILLEGIBLE\]/i.test(value);
      return `<dt>${escapeHtml(k.replace(/_/g, ' '))}</dt>` +
             `<dd${redacted ? ' class="redacted"' : ''}>${escapeHtml(value)}</dd>`;
    });
  return rows.join('') || '<dt>—</dt><dd>No further properties recorded.</dd>';
}

/** A schema node is a *type*, so its detail is the contract: what it means,
 *  which properties it carries, and how many records exist. */
function showSchemaDetails(label) {
  const node = state.schema.nodes.find((n) => n.id === label);
  if (!node) return;
  state.selected = label;
  openDetails(node.label, state.meta.colors[node.label] ?? '#8894a8');
  $('detail-group').textContent = node.group ? `POLE · ${node.group}` : '';
  $('detail-name').textContent = node.label;
  $('detail-status').hidden = true;
  $('detail-description').textContent = node.description ?? '';
  $('detail-props').innerHTML =
    `<dt>Records</dt><dd>${node.count}</dd>` +
    // `||` not `??`: the schema library defaults an absent description to an
    // empty string, which nullish-coalescing happily renders as a blank row.
    node.properties.map((p) =>
      `<dt>${escapeHtml(p.name)}</dt>` +
      `<dd>${escapeHtml(p.description || p.type.toLowerCase())}</dd>`).join('');

  const edges = state.schema.relationships.filter((r) => r.from === label || r.to === label);
  $('detail-rels').innerHTML = edges.map((r) => {
    const outgoing = r.from === label;
    return `<li class="inert"><span class="rel-type">${outgoing ? '→' : '←'} ${r.type}</span>` +
           `<span class="dir">${escapeHtml(outgoing ? r.to : r.from)}</span> ` +
           `${escapeHtml(r.description ?? '')}</li>`;
  }).join('') || '<li class="inert">No patterns declared for this type.</li>';
  state.renderer.select(label);
}

/** A retrieved passage is raw source text, not a graph record — it has no
 *  evidence level and no relationships of its own worth listing. */
function showChunkDetails(node) {
  state.selected = node.id;
  openDetails('Passage', CHUNK_COLOR);
  $('detail-group').textContent = 'Source text';
  $('detail-name').textContent = node.source ?? 'Retrieved passage';
  $('detail-status').hidden = true;
  $('detail-description').textContent = node.text ?? node.description ?? '';
  $('detail-props').innerHTML = node.score
    ? `<dt>Score</dt><dd>${node.score.toFixed(3)}</dd>`
    : '';
  $('detail-rels').innerHTML =
    '<li class="inert">The records extracted from this passage are the next ring out.</li>';
  state.renderer.select(node.id);
}

function openDetails(label, color) {
  $('detail-label').textContent = label ?? 'Record';
  $('detail-label').style.background = color;
  $('details').hidden = false;
  $('app').classList.add('with-details');
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
async function streamEvents(path, init, onEvent) {
  const res = await fetch(path, init);
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

const postJson = (body) => ({
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

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

function resetProgress(steps = PROGRESS_STEPS) {
  const ol = $('progress-steps');
  ol.innerHTML = Array.from({ length: steps }, () => '<li></li>').join('');
  $('progress').hidden = false;
}

/** Advance the indicator: everything before `index` is done, `index` is live. */
function markProgress(index) {
  const items = [...$('progress-steps').children];
  items.forEach((li, i) => {
    li.classList.toggle('is-done', i < index);
    li.classList.toggle('is-live', i === index);
  });
}

function finishProgress() {
  for (const li of $('progress-steps').children) {
    li.classList.add('is-done');
    li.classList.remove('is-live');
  }
  setStage(null);
}

function closeAnswer() {
  $('answer').hidden = true;
  $('examples').hidden = false;
  $('context-details').hidden = false;
  $('answer-body').className = '';
  setStage(null);
  state.unfoldNodes = new Map();
  syncInsets();
}

async function askQuestion() {
  const question = $('question').value.trim();
  if (!question) return;
  if (state.view !== 'graph') await setView('graph');

  const btn = $('ask-button');
  btn.disabled = true;
  btn.textContent = 'Working';
  $('answer').hidden = false;
  $('examples').hidden = true;
  $('answer-title').textContent = 'Answer';
  $('answer-body').className = '';
  $('context-details').hidden = false;
  syncInsets();
  $('answer-body').innerHTML = '';
  $('answer-context').innerHTML = '';
  // The note describes the standing view ("Sensor: 3 direct connections"), which
  // is not what is on screen once an unfold starts.
  setNote(null);
  resetProgress();
  let step = 0;
  markProgress(step);
  setStage('Sending the question…');

  // The standing graph is ghosted when the first ring is ready, not now. The
  // fixed retrievers deliver that within a second, so the effect is unchanged;
  // the agent chooses its own route and can take a minute, and ghosting up
  // front would leave an empty stage for all of it.
  state.unfoldNodes = new Map();

  const beat = beatQueue(640);
  let answered = false;
  let gotRings = false;
  let ghosted = false;
  const ghostOnce = () => {
    if (!ghosted) { state.renderer.beginUnfold(); ghosted = true; }
  };

  try {
    await streamEvents('/api/ask/stream',
      postJson({ question, retriever: $('retriever').value, top_k: 5 }),
      (name, data) => {
        if (name === 'stage') {
          beat.push(() => { setStage(data.label); markProgress(Math.min(step++, PROGRESS_STEPS - 1)); });
        } else if (name === 'unfold') {
          gotRings = true;
          beat.push(() => {
            ghostOnce();
            setStage(data.label);
            markProgress(Math.min(step++, PROGRESS_STEPS - 1));
            for (const n of data.nodes) state.unfoldNodes.set(n.id, n);
            state.renderer.addStage({
              nodes: data.nodes,
              relationships: data.relationships ?? [],
              stage: STAGE_RING[data.stage] ?? 1,
            });
          });
        } else if (name === 'answer') {
          answered = true;
          beat.push(() => {
            finishProgress();
            $('answer-body').innerHTML = markEvidence(renderMarkdown(data.answer));
            $('answer-context').innerHTML = data.context.length
              ? data.context.map((c) => `<pre>${escapeHtml(c)}</pre>`).join('')
              : '<pre>(no context returned)</pre>';
            syncInsets();
          });
        } else if (name === 'warning') {
          console.warn(data.message);
        } else if (name === 'error') {
          throw new Error(data.message);
        }
      });
    if (!answered) throw new Error('the stream ended before the answer arrived');
  } catch (err) {
    console.error(err);
    finishProgress();
    $('progress').hidden = true;
    // A request that produced no rings at all leaves the graph ghosted with
    // nothing to look at. Put it back rather than stranding the viewer.
    if (!gotRings && ghosted) {
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

/* ---------------- extending the graph ---------------- */

function logUpload(text, cls = '') {
  const ul = $('upload-log');
  ul.hidden = false;
  for (const li of ul.querySelectorAll('.is-live')) li.classList.remove('is-live');
  const li = document.createElement('li');
  li.className = cls;
  li.textContent = text;
  ul.appendChild(li);
  ul.scrollTop = ul.scrollHeight;
  return li;
}

async function uploadDocument(file) {
  if (!file) return;
  const zone = $('drop-zone');
  zone.classList.add('is-busy');
  $('upload-log').innerHTML = '';
  logUpload(`${file.name} · ${Math.max(1, Math.round(file.size / 1024))} KB`);

  if (state.view !== 'graph') await setView('graph');

  const body = new FormData();
  body.append('file', file);
  let added = 0;
  try {
    await streamEvents('/api/documents', { method: 'POST', body }, (name, data) => {
      if (name === 'stage') {
        logUpload(data.label, 'is-live');
      } else if (name === 'unfold') {
        logUpload(data.label);
        state.renderer.beginUnfold();
        for (const n of data.nodes) state.unfoldNodes.set(n.id, n);
        state.renderer.addStage({
          nodes: data.nodes,
          relationships: data.relationships ?? [],
          stage: 1,
        });
      } else if (name === 'done') {
        added = data.added;
        state.newIds = new Set(data.newIds);
        state.meta.counts = data.counts;
      } else if (name === 'error') {
        throw new Error(data.message);
      }
    });
    logUpload(`${added} records added — filters and counts updated`);
    // The graph behind the unfold is now stale, and so is every count in the
    // rail. Refresh both, but leave the new records lit: what the document
    // added is the whole point of having uploaded it.
    state.meta = { ...state.meta, ...(await api('/api/meta')) };
    buildPoleFilters();
    buildStats();
    updateHud();
    loadSources();
  } catch (err) {
    console.error(err);
    logUpload(err.message, 'is-error');
  } finally {
    zone.classList.remove('is-busy');
    $('upload-input').value = '';
  }
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
          `<span class="dot" style="width:7px;height:7px;border-radius:50%;flex:none;` +
          `background:${state.meta.colors[n.label] ?? '#8894a8'}"></span>` +
          `<span>${escapeHtml(n.name)}<br><span class="r-label">${escapeHtml(n.label ?? '')}</span></span>`;
        li.onclick = async () => {
          list.hidden = true;
          $('search').value = '';
          if (state.view !== 'graph') await setView('graph');
          state.renderer.focus(n.id);
          showDetails(n.id);
        };
        list.appendChild(li);
      }
      list.hidden = res.nodes.length === 0;
    } catch (err) { console.error(err); }
  }, 180);
}

/* ---------------- text rendering ---------------- */

/** Minimal markdown -> HTML. Models emit **bold**, `code`, links and bullet
 *  lists whether or not you ask for prose; rendering literal asterisks looks
 *  broken. Escapes first, so this never introduces markup from model output. */
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
    // Links first: the label can itself contain emphasis, and rewriting the
    // emphasis first would leave tags inside the bracket match.
    .replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, (_, label, href) =>
      `<a href="${href}" target="_blank" rel="noreferrer noopener">${label}</a>`)
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*]+)\*/g, '$1<em>$2</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
}

/** Colour the evidence words the model is instructed to emit, where the corpus
 *  grades evidence at all. */
function markEvidence(html) {
  if (!state.meta.gradesEvidence) return html;
  return html.replace(/\[?\b(confirmed|reported|rumou?red)\b\]?/gi, (m) => {
    const key = /rumou?red/i.test(m) ? 'rumored' : m.replace(/[[\]]/g, '').toLowerCase();
    return `<span class="ev ev-${key}">${m}</span>`;
  });
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

/* ---------------- wiring ---------------- */

function wireEvents() {
  $('ask-form').addEventListener('submit', (e) => { e.preventDefault(); askQuestion(); });
  $('search').addEventListener('input', onSearch);
  $('close-details').addEventListener('click', hideDetails);
  $('close-answer').addEventListener('click', async () => {
    // Back to the whole graph, whatever was on screen when the question was
    // asked. Restoring a one-record neighbourhood there reads as the graph
    // having vanished.
    closeAnswer();
    // Collapse first, from memory, so the standing graph is back the instant
    // the button is clicked; the refresh that follows re-syncs it with the
    // server, which on a remote Aura instance can take a few seconds.
    state.renderer?.collapse();
    await setGraphMode('all');
  });
  $('reset-view').addEventListener('click', async () => {
    closeAnswer();
    state.newIds = new Set();
    state.graphMode = 'all';
    state.drilledInto = null;
    state.focused = null;
    await setView('graph');
  });
  for (const b of document.querySelectorAll('#graph-mode button')) {
    b.addEventListener('click', () => setGraphMode(b.dataset.mode));
  }
  for (const tab of document.querySelectorAll('.view-tab')) {
    tab.addEventListener('click', () => setView(tab.dataset.view));
  }

  $('isolated-toggle').addEventListener('click', (e) => {
    state.showIsolated = !state.showIsolated;
    e.currentTarget.classList.toggle('is-off', !state.showIsolated);
    refreshGraph();
  });

  const zone = $('drop-zone');
  $('upload-input').addEventListener('change', (e) => uploadDocument(e.target.files[0]));
  zone.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); $('upload-input').click(); }
  });
  // The whole window is a drop target for dragover so the browser never takes
  // over and navigates to the dropped file, which silently ends the session.
  for (const type of ['dragenter', 'dragover']) {
    window.addEventListener(type, (e) => {
      e.preventDefault();
      if (e.target.closest?.('#drop-zone')) zone.classList.add('is-dragover');
    });
  }
  window.addEventListener('dragleave', (e) => {
    if (!e.relatedTarget || !e.relatedTarget.closest?.('#drop-zone')) {
      zone.classList.remove('is-dragover');
    }
  });
  window.addEventListener('drop', (e) => {
    e.preventDefault();
    zone.classList.remove('is-dragover');
    if (e.target.closest?.('#drop-zone')) uploadDocument(e.dataTransfer?.files?.[0]);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { hideDetails(); $('search-results').hidden = true; }
  });
}

boot();

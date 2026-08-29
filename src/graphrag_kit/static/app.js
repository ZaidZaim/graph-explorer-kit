/* Graph explorer front-end.
 *
 * NVL ships ESM-only with no UMD bundle, so it is imported from esm.sh rather
 * than bundled. If that import fails (offline, CDN blocked), renderer.js falls
 * back to a built-in canvas renderer so the demo still works.
 */

import { createRenderer } from '/static/renderer.js?v=2';

const $ = (id) => document.getElementById(id);
const api = async (path, opts) => {
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(`${path} -> ${res.status} ${await res.text()}`);
  return res.json();
};

const state = {
  meta: null,
  graph: { nodes: [], relationships: [] },
  activeLabels: new Set(),
  activeStatuses: new Set(),
  renderer: null,
  selected: null,
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
      colors: state.meta.colors,
    });

    syncInsets();
    window.addEventListener('resize', syncInsets);
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
  let left = 0;
  if (!answer.hidden) {
    const r = answer.getBoundingClientRect();
    left = Math.max(0, r.right - stage.left + 16);
  }
  const bottom = askBar ? stage.bottom - askBar.getBoundingClientRect().top + 16 : 0;
  state.renderer?.setInsets({ left, bottom: Math.max(0, bottom) });
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
    ?? (await api(`/api/expand?id=${encodeURIComponent(nodeId)}`)).nodes.find((n) => n.id === nodeId);
  if (!node) return;

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

function hideDetails() {
  state.selected = null;
  $('details').hidden = true;
  $('app').classList.remove('with-details');
  state.renderer?.select(null);
}

/* ---------------- ask ---------------- */

async function askQuestion() {
  const question = $('question').value.trim();
  if (!question) return;

  const btn = $('ask-button');
  btn.disabled = true;
  btn.textContent = 'Thinking…';
  $('answer').hidden = false;
    syncInsets();
  $('answer-body').textContent = 'Retrieving from the graph…';
  $('answer-context').innerHTML = '';

  try {
    const res = await api('/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question,
        retriever: $('retriever').value,
        top_k: 5,
      }),
    });

    $('answer-body').innerHTML = markEvidence(renderMarkdown(res.answer));
    $('answer-context').innerHTML = res.context.length
      ? res.context.map((c) => `<pre>${escapeHtml(c)}</pre>`).join('')
      : '<pre>(no context returned)</pre>';

    // Unfold the evidence: the graph re-lays itself as a radial tree with the
    // chunks that answered the question at the centre, opening ring by ring.
    if (res.subgraph.nodes.length) {
      state.renderer.unfold(res.subgraph);
    } else {
      state.renderer.collapse();
    }
  } catch (err) {
    console.error(err);
    $('answer-body').textContent = `Request failed: ${err.message}`;
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
  const ids = res.nodes.map((n) => n.id);
  state.renderer.unfold({ nodes: res.nodes, relationships: [], seeds: ids });
  $('answer').hidden = false;
    syncInsets();
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
    state.renderer?.collapse();
  });
  $('reset-view').addEventListener('click', async () => {
    $('answer').hidden = true;
    syncInsets();
    await refreshGraph();
  });
  $('show-timeline').addEventListener('click', showTimeline);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { hideDetails(); $('search-results').hidden = true; }
  });
}

boot();

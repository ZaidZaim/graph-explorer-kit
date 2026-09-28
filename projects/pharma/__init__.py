"""Pharma Pipeline — a molecule-to-market knowledge graph over company disclosures.

The graph this project reads was built with Neo4j Document Intelligence from
four public investor documents: AbbVie's long-term guidance and pipeline update
(February 2024), Bristol Myers Squibb's Q1 2024 results deck, Johnson &
Johnson's 2Q 2024 pipeline chart, and Bayer's pharmaceuticals R&D pipeline
overview (July 2025). This package puts the `neo4j-graphrag` engine on top of
it — retrieval, an agent, an explorer, and ingestion for decks added later.

    GRAPHRAG_PROJECT=projects.pharma

The lens is the path a drug takes from bench to market, in six groups:

  MOLECULE      what is being developed and what it acts on — Drug, Target,
                Gene, Protein.
  INDICATION    who it is for — Disease, Population, and the AdverseEvents
                reported along the way.
  TRIAL         the Study that tests it.
  REGULATORY    the RegulatoryEvent that lets it be sold: submission, PDUFA
                date, approval.
  COMMERCIAL    who owns it and what it earns — Organization,
                FinancialProjection.
  RECORD        the provenance layer. A pipeline deck is a company *asserting*
                things about its own programmes, and the assertion is kept as
                an Evidence node with the document it came from; Abbreviation
                and Concept hold the vocabulary the decks are written in.

The labels stay the domain's own — Population is not merged into Disease and
Target is not merged into Protein — because the distinctions carry the
analysis. The lens is placed over them, not put in their place.

On forward-looking statements: nothing in this project turns a projection
into an outcome. "Approval anticipated 2025" is stored as the company's
expectation, dated as printed, and answered as such. The corpus records what
companies disclosed, attributed to the document that discloses it.
"""

from __future__ import annotations

from pathlib import Path

from graphrag_kit.project import LexicalSpec, ProjectSpec
from projects.pharma.schema import PHARMA_SCHEMA

# Held to the same standard as the graph Document Intelligence built, so a deck
# dropped on the explorer's "Extend the graph" lands in the same shape.
EXTRACTION_RULES = """
Corpus-specific rules:
- These are company disclosures: pipeline charts, quarterly results decks,
  guidance updates. Extract what the company states, attributed to it. Never
  infer an efficacy result, an approval, or an outcome the document does not
  state.
- Forward-looking statements ("anticipated", "expected", "projected") are the
  company's projections. Keep the hedge in the `description`, and in
  RegulatoryEvent.date and Study.status exactly as printed
  ("Approval anticipated 2025", "Expected data readout 2024").
- Organization: one node per company, named as the document names it
  ("Bristol Myers Squibb", "AbbVie", "Bayer", "Johnson & Johnson"). Partners,
  licensors, acquisition targets, regulators and data providers are
  Organizations too.
- Drug: `name` is the brand or programme name as printed (Opdivo, KarXT,
  ABBV-400, BAY 2701250); `identifier` is the code or INN where given, else the
  name. `modality` (Small Molecule, Antibody, Antibody Drug Conjugate, Cell
  Therapy, Genetic Medicine, Radionuclide Therapy) and `mechanism_of_action`
  (PD1 inhibitor, IL-23, M1/M4 agonist) only where the document states them.
- Study: `identifier` is the NCT number where printed, else the trial name or
  code; `name` is the trial name (CheckMate -8HW, OCEANIC-STROKE). Normalise
  `phase` to "Phase I", "Phase I/II", "Phase II" or "Phase III".
- Disease is the indication in the document's own words. The line of therapy
  or biomarker subgroup ("2L+", "PD-L1+") belongs on a Population, not in the
  Disease name.
- Target is the biological target (PD-1, LAG-3, CCR8, Factor XIa). Emit Gene
  or Protein only where the document names one as such with an identifier.
- Every statement is an Evidence node: `assertion_type` from TREATS,
  INVESTIGATED_FOR_INDICATION_IN_STUDY, HAS_TARGET, HAS_MECHANISM_OF_ACTION,
  REGULATORY_MILESTONE, FINANCIAL_PROJECTION, CAUSES_ADVERSE_EVENT,
  PRESENTS_DATA or PARTNERS_WITH; `source_document` the deck's title as
  printed; `description` the statement in one sentence. Then link it with the
  matching ASSERTED_ABOUT_* relationship to every entity it concerns.
- RegulatoryEvent: name it by what happened or is expected ("U.S. approval",
  "EU submission", "PDUFA"); `type` from Approval, Submission, Registration,
  PDUFA, Priority Review or Data Readout; `date` exactly as printed
  ("2024-06-21", "Nov 2023", "2H 2025"). Never invent precision.
- FinancialProjection: `type` is the line item as printed ("Global Net Sales",
  "Diluted EPS", "Gross Margin %"), `year` the fiscal year, `value` the number
  without units, `currency` where stated.
- Abbreviation: every abbreviation the document defines (PFS, NSCLC, MIUC),
  with `short_form` and `full_form`, linked with HAS_FULL_FORM_* to the entity
  it expands to where that entity exists, else with HAS_FULL_FORM to a Concept.
- Slide furniture is not an entity: page numbers, footnote markers, trademark
  symbols, and the forward-looking-statements boilerplate.
"""

PROJECT = ProjectSpec(
    key="pharma",
    title="PHARMA PIPELINE",
    subtitle="AbbVie · BMS · J&J · Bayer · pipeline disclosures",
    schema=PHARMA_SCHEMA,
    data_dir=Path(__file__).resolve().parent / "data",
    extraction_rules=EXTRACTION_RULES,
    rag_persona=(
        "You are a pipeline analyst answering questions about pharmaceutical "
        "companies' own disclosures — investor presentations, R&D pipeline "
        "updates, quarterly results — from a knowledge graph of drugs, targets, "
        "indications, studies, regulatory milestones, financial figures and the "
        "companies behind them. Report what a company disclosed, attributed to "
        "the document that discloses it. A forward-looking statement is the "
        "company's projection, not an outcome: keep 'anticipated', 'expected' "
        "and 'projected' where the source has them. Do not infer efficacy or "
        "approval status the documents do not state, and do not give investment "
        "advice."
    ),
    # --- molecule to market ----------------------------------------------
    groups={
        "MOLECULE": ("Drug", "Target", "Gene", "Protein"),
        "INDICATION": ("Disease", "Population", "AdverseEvent"),
        "TRIAL": ("Study",),
        "REGULATORY": ("RegulatoryEvent",),
        "COMMERCIAL": ("Organization", "FinancialProjection"),
        "RECORD": ("Evidence", "Abbreviation", "Concept"),
    },
    groups_title="Molecule to market",
    group_colors={
        "MOLECULE": "#2DD4BF",
        "INDICATION": "#FB7185",
        "TRIAL": "#A78BFA",
        "REGULATORY": "#FBBF24",
        "COMMERCIAL": "#60A5FA",
        "RECORD": "#94A3B8",
    },
    # Within a group, the secondary labels are shaded so a Target reads as a
    # kind of molecule at a glance without leaving the group's colour.
    palette={
        "Target": "#14B8A6",
        "Gene": "#0D9488",
        "Protein": "#0F766E",
        "Population": "#E8607D",
        "AdverseEvent": "#BE4B5F",
        "FinancialProjection": "#3B82F6",
        "Evidence": "#CBD5E1",
        "Abbreviation": "#7E8CA3",
        "Concept": "#5F6E85",
    },
    # Drug, Study, Disease, Target, Gene, Protein, AdverseEvent,
    # RegulatoryEvent, Organization and Concept carry `name`. An Abbreviation is
    # its short form, a Population is its description, an Evidence node is its
    # statement (or, failing that, what kind of statement it is), and a
    # FinancialProjection is the line item it reports.
    name_properties=("name", "short_form", "description", "assertion_type", "type", "identifier"),
    date_property="date",
    # No evidence grading: a company deck does not rate its own statements, and
    # a confidence score per record would be exactly the inference the
    # extraction rules forbid. Provenance does the job instead — every
    # statement is an Evidence node tied to the passage and the document it
    # came from. (Study.status is a trial status, not an evidence level; with
    # grading off the engine never reads it as one.)
    evidence_levels=(),
    # Document Intelligence built this graph; this project reads and extends it.
    # Entity resolution is never run across the whole of it: DI kept same-named
    # records apart where the documents did, and a global exact-name merge
    # would silently destroy that — irreversibly.
    owns_graph=False,
    # Across documents, only these carry identity in their name. A
    # RegulatoryEvent called "U.S. approval" recurs on every pipeline slide and
    # is a different milestone each time; a Population is a description; an
    # Evidence node is a statement; a FinancialProjection is a line item that
    # every deck has one of.
    cross_document_labels=(
        "Organization",
        "Drug",
        "Disease",
        "Target",
        "Gene",
        "Protein",
        "Study",
        "AdverseEvent",
        "Concept",
    ),
    # Decks say "the Company" for themselves and "Undisclosed" for a target
    # they are not naming; neither is a name two records can share.
    placeholder_names=(
        "[REDACTED]",
        "unknown",
        "n/a",
        "none",
        "the company",
        "undisclosed",
        "tbd",
    ),
    lexical=LexicalSpec(
        # Document Intelligence embedded these chunks with a 3072-dim model of
        # its own, under `embedding`, with a vector index already on it. That
        # index is left exactly as it is: our embeddings go in a property beside
        # it, because two models' vectors in one index score ~0.5 against each
        # other — cosine zero, dressed up as a similarity.
        embedding_property="openai_embedding",
        # DI's chunks. `graphrag-adopt` adds :Chunk alongside, which is the only
        # structural write this project makes to the existing graph.
        adopted_chunk_label="__Chunk__",
        # DI's source-file nodes.
        source_label="__Document__",
        source_name_properties=("source", "path"),
        # Both conventions are read through one pattern: DI's names, and the
        # ones SimpleKGPipeline writes for decks uploaded later.
        entity_to_chunk="FROM_CHUNK|__NODE_TO_CHUNK__",
        chunk_to_source="FROM_DOCUMENT|__CHUNK_TO_DOCUMENT__",
        entity_text_properties=(
            "name",
            "description",
            "identifier",
            "short_form",
            "full_form",
            "mechanism_of_action",
            "assertion_type",
        ),
    ),
    text2cypher_examples=[
        "USER INPUT: 'Which drugs does AbbVie develop?' "
        "QUERY: MATCH (o:Organization)-[:DEVELOPS|CO_DEVELOPS|LICENSES]->(d:Drug) "
        "WHERE toLower(o.name) CONTAINS 'abbvie' "
        "RETURN DISTINCT d.name, d.modality, d.mechanism_of_action",
        "USER INPUT: 'Which drugs are linked to schizophrenia, and by which company?' "
        "QUERY: MATCH (e:Evidence)-[:ASSERTED_ABOUT_DISEASE]->(dis:Disease) "
        "WHERE toLower(dis.name) CONTAINS 'schizophrenia' "
        "MATCH (e)-[:ASSERTED_ABOUT_DRUG]->(d:Drug) "
        "OPTIONAL MATCH (o:Organization)-[:DEVELOPS|CO_DEVELOPS|LICENSES]->(d) "
        "RETURN DISTINCT d.name, o.name AS company, e.assertion_type, e.description",
        "USER INPUT: 'What does Bristol Myers Squibb have in Phase III?' "
        "QUERY: MATCH (o:Organization)-[:CONDUCTS]->(s:Study) "
        "WHERE o.name IN ['Bristol Myers Squibb', 'BMS'] "
        "AND s.phase IN ['Phase III', 'Phase 3', 'Ph3'] "
        "RETURN s.name, s.identifier, s.status, s.primary_completion_date",
        "USER INPUT: 'How many studies are there per phase?' "
        "QUERY: MATCH (s:Study) RETURN coalesce(s.phase, 'not stated') AS phase, "
        "count(*) AS studies ORDER BY studies DESC",
        "USER INPUT: 'Which regulatory decisions were expected in 2024?' "
        "QUERY: MATCH (r:RegulatoryEvent) WHERE r.date CONTAINS '2024' "
        "OPTIONAL MATCH (e:Evidence)-[:ASSERTED_ABOUT_REGULATORY_EVENT]->(r) "
        "OPTIONAL MATCH (e)-[:ASSERTED_ABOUT_DRUG]->(d:Drug) "
        "RETURN r.name, r.type, r.date, collect(DISTINCT d.name) AS drugs ORDER BY r.date",
        "USER INPUT: 'Which companies partner with, or acquired, which?' "
        "QUERY: MATCH (a:Organization)-[r:PARTNERS_WITH|ACQUIRED]->(b:Organization) "
        "RETURN a.name, type(r) AS how, b.name",
        "USER INPUT: 'What does MIUC stand for?' "
        "QUERY: MATCH (a:Abbreviation) WHERE toUpper(a.short_form) = 'MIUC' "
        "RETURN a.short_form, a.full_form",
        "USER INPUT: 'What sales figures are given for 2025?' "
        "QUERY: MATCH (f:FinancialProjection) WHERE f.year = '2025' "
        "RETURN f.type, f.value, f.currency ORDER BY f.type",
        "USER INPUT: 'Which targets have more than one drug against them?' "
        "QUERY: MATCH (e:Evidence)-[:ASSERTED_ABOUT_TARGET]->(t:Target), "
        "(e)-[:ASSERTED_ABOUT_DRUG]->(d:Drug) "
        "WITH t, collect(DISTINCT d.name) AS drugs WHERE size(drugs) > 1 "
        "RETURN t.name, t.type, drugs ORDER BY size(drugs) DESC",
    ],
    # Four, not six: each is a sentence, and six wrap to four rows of chips.
    example_questions=[
        "Which companies have programmes in Parkinson's disease, and what are they?",
        "What does Bristol Myers Squibb have in Phase III?",
        "Which regulatory decisions were expected in 2024?",
        "Which diseases are being pursued by more than one company, and by whom?",
    ],
    theme_css=Path(__file__).resolve().parent / "theme.css",
)

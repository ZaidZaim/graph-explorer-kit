"""Pharma pipeline schema, as the graph actually holds it.

Written against the live `PharmaDemo` instance rather than from first
principles: every label, property and relationship below was observed in the
graph that Neo4j Document Intelligence built from the four pipeline and
results decks. Keeping the schema honest to the data matters twice over —
Text2CypherRetriever generates queries against it, and the extractor for newly
uploaded documents is held to it, so a property that does not exist in the
graph becomes a query that returns nothing and an extraction that writes a
field no query will ever read.

Two things about the shape are worth knowing before reading the patterns.

First, assertions are reified. The graph does not say `(Drug)-[:TREATS]->
(Disease)`; it says `(Evidence {assertion_type: 'TREATS'})` with an
`ASSERTED_ABOUT_DRUG` edge to the drug and an `ASSERTED_ABOUT_DISEASE` edge to
the disease. Document Intelligence did that so the statement itself — who said
it, in which document — is a node. "Which drugs are linked to schizophrenia?"
is therefore a two-edge pattern through Evidence, and the few-shot Cypher in
`__init__.py` shows the model that pattern.

Second, abbreviations resolve to typed targets. `(:Abbreviation {short_form:
'NSCLC'})-[:HAS_FULL_FORM_DISEASE]->(:Disease)`, and the same for Target,
Organization, Drug, AdverseEvent, Gene, Protein and RegulatoryEvent, with the
bare `HAS_FULL_FORM` landing on a `Concept` when the expansion is not one of
the schema's own kinds. Pipeline decks are written in abbreviations — PFS,
MIUC, 2L+ — so this layer is what makes them readable.

The molecule-to-market grouping lives in the ProjectSpec (see __init__.py),
not here: the labels are the domain's own, and the lens is placed over them.
"""

from __future__ import annotations

from neo4j_graphrag.components.schema import (
    GraphSchema,
    NodeType,
    PropertyType,
    RelationshipType,
)

_NAME = PropertyType(name="name", type="STRING", description="Name as printed in the document")

PHARMA_SCHEMA = GraphSchema(
    node_types=[
        # --- the molecule -------------------------------------------------
        NodeType(
            label="Drug",
            description=(
                "A marketed product or pipeline programme: a brand (Opdivo, "
                "Skyrizi), a code (ABBV-400, BAY 2701250) or a compound name."
            ),
            properties=[
                _NAME,
                PropertyType(
                    name="identifier",
                    type="STRING",
                    description="Programme code or INN where given, else the name",
                ),
                PropertyType(
                    name="modality",
                    type="STRING",
                    description=(
                        "e.g. 'Small Molecule', 'Antibody', 'Antibody Drug Conjugate', "
                        "'Cell Therapy', 'Genetic Medicine', 'Radionuclide Therapy'"
                    ),
                ),
                PropertyType(
                    name="mechanism_of_action",
                    type="STRING",
                    description="e.g. 'PD1 inhibitor', 'IL-23', 'M1/M4 agonist'",
                ),
            ],
        ),
        NodeType(
            label="Target",
            description="The biological target a drug acts on: PD-1, LAG-3, CCR8, Factor XIa.",
            properties=[
                _NAME,
                PropertyType(
                    name="type",
                    type="STRING",
                    description="e.g. 'Protein', 'Receptor', 'Enzyme', 'Cytokine', 'Antigen'",
                ),
            ],
        ),
        NodeType(
            label="Gene",
            description="A gene named as such, with an identifier.",
            properties=[
                _NAME,
                PropertyType(name="ncbi_gene_id", type="STRING", description="NCBI Gene id"),
            ],
        ),
        NodeType(
            label="Protein",
            description="A protein named as such, with an identifier.",
            properties=[
                _NAME,
                PropertyType(name="uniprot_id", type="STRING", description="UniProt accession"),
            ],
        ),
        # --- the indication -----------------------------------------------
        NodeType(
            label="Disease",
            description=(
                "An indication as the document words it: 'Non-Small Cell Lung "
                "Cancer', 'psoriatic arthritis', 'Schizophrenia'."
            ),
            properties=[_NAME],
        ),
        NodeType(
            label="Population",
            description=(
                "A patient population a study or a market claim is about: "
                "'2L+ NSCLC patients', '1.6M adults treated for schizophrenia in the U.S.'"
            ),
            properties=[
                PropertyType(
                    name="description",
                    type="STRING",
                    description="The population in the document's words",
                ),
                PropertyType(
                    name="size", type="STRING", description="Number of patients, as a number"
                ),
            ],
        ),
        NodeType(
            label="AdverseEvent",
            description=(
                "A safety finding the document reports: 'weight gain', 'extrapyramidal symptoms'."
            ),
            properties=[_NAME],
        ),
        # --- the trial ----------------------------------------------------
        NodeType(
            label="Study",
            description=(
                "A clinical trial: named (CheckMate -8HW, OCEANIC-STROKE) or coded "
                "(NCT04008030, CA056-015)."
            ),
            properties=[
                _NAME,
                PropertyType(
                    name="identifier",
                    type="STRING",
                    description="NCT number where printed, else the trial name or code",
                ),
                PropertyType(
                    name="phase",
                    type="STRING",
                    description="'Phase I', 'Phase I/II', 'Phase II', 'Phase III'",
                ),
                PropertyType(
                    name="status",
                    type="STRING",
                    description=(
                        "As printed: 'Recruiting', 'Study ongoing', 'Expected data "
                        "readout 2025', 'Did not meet primary endpoint'"
                    ),
                ),
                PropertyType(
                    name="primary_completion_date",
                    type="STRING",
                    description="As printed, e.g. 'Q4 2025'",
                ),
            ],
        ),
        # --- the regulator ------------------------------------------------
        NodeType(
            label="RegulatoryEvent",
            description=(
                "A milestone with a regulator, happened or anticipated: an approval, "
                "a submission, a PDUFA date, a registration."
            ),
            properties=[
                _NAME,
                PropertyType(
                    name="type",
                    type="STRING",
                    description=(
                        "'Approval', 'Submission', 'Registration', 'PDUFA', "
                        "'Priority Review', 'Data Readout'"
                    ),
                ),
                PropertyType(
                    name="date",
                    type="STRING",
                    description=(
                        "As printed and no more precise: '2024-06-21', 'Nov 2023', "
                        "'2025'. Anticipated dates are still dates."
                    ),
                ),
            ],
        ),
        # --- the business -------------------------------------------------
        NodeType(
            label="Organization",
            description=(
                "A company, partner, regulator, society or data provider: AbbVie, "
                "Bristol Myers Squibb, Bayer, Johnson & Johnson, Cerevel, FDA, IQVIA."
            ),
            properties=[
                _NAME,
                PropertyType(
                    name="type",
                    type="STRING",
                    description=(
                        "'Pharmaceutical Company', 'Biotechnology Company', "
                        "'Regulatory Agency', 'Professional Society', 'Data Provider'"
                    ),
                ),
            ],
        ),
        NodeType(
            label="FinancialProjection",
            description=(
                "One number from a results or guidance slide: sales, EPS, margin, "
                "share, tax rate — reported or projected."
            ),
            properties=[
                PropertyType(
                    name="type",
                    type="STRING",
                    description=(
                        "The line item as printed: 'Global Net Sales', 'Diluted EPS', "
                        "'Gross Margin %'"
                    ),
                ),
                PropertyType(name="year", type="STRING", description="Fiscal year"),
                PropertyType(name="value", type="STRING", description="The number, without units"),
                PropertyType(name="currency", type="STRING", description="'USD' where stated"),
            ],
        ),
        # --- the record itself --------------------------------------------
        NodeType(
            label="Evidence",
            description=(
                "One statement the document makes, kept as a node so that what was "
                "asserted, and where, stays visible. It points at every entity it "
                "concerns through ASSERTED_ABOUT_* edges."
            ),
            properties=[
                PropertyType(
                    name="assertion_type",
                    type="STRING",
                    description=(
                        "What kind of statement: 'TREATS', "
                        "'INVESTIGATED_FOR_INDICATION_IN_STUDY', 'HAS_TARGET', "
                        "'REGULATORY_MILESTONE', 'FINANCIAL_PROJECTION', "
                        "'CAUSES_ADVERSE_EVENT', 'PRESENTS_DATA'"
                    ),
                ),
                PropertyType(
                    name="source_document",
                    type="STRING",
                    description="The deck or section the statement comes from, as titled",
                ),
                PropertyType(
                    name="description",
                    type="STRING",
                    description="The statement in one sentence, in the document's terms",
                ),
                PropertyType(name="publication_date", type="STRING"),
                PropertyType(name="valid_from", type="STRING"),
                PropertyType(
                    name="provenance_description",
                    type="STRING",
                    description="A cited source for the figure, e.g. 'Rx Source: IQVIA'",
                ),
            ],
        ),
        NodeType(
            label="Abbreviation",
            description="An abbreviation the document uses, with its expansion.",
            properties=[
                PropertyType(
                    name="short_form", type="STRING", description="'PFS', 'NSCLC', 'MIUC'"
                ),
                PropertyType(
                    name="full_form", type="STRING", description="'Progression Free Survival'"
                ),
            ],
        ),
        NodeType(
            label="Concept",
            description=(
                "A named thing that is none of the above: a congress (ASCO GI), a "
                "country, a therapeutic area, a metric."
            ),
            properties=[_NAME, PropertyType(name="description", type="STRING")],
        ),
    ],
    relationship_types=[
        # Who does what.
        RelationshipType(label="DEVELOPS", description="A company develops or markets a drug"),
        RelationshipType(
            label="CO_DEVELOPS", description="A company develops a drug jointly with another"
        ),
        RelationshipType(
            label="LICENSES", description="A company in-licenses or out-licenses a drug"
        ),
        RelationshipType(label="CONDUCTS", description="A company sponsors or runs a study"),
        RelationshipType(label="PARTNERS_WITH", description="A stated collaboration"),
        RelationshipType(
            label="ACQUIRED", description="A company acquired, or is acquiring, another"
        ),
        # What a statement is about.
        RelationshipType(
            label="ASSERTED_ABOUT_DRUG", description="The statement concerns this drug"
        ),
        RelationshipType(
            label="ASSERTED_ABOUT_DISEASE", description="The statement concerns this indication"
        ),
        RelationshipType(
            label="ASSERTED_ABOUT_STUDY", description="The statement concerns this study"
        ),
        RelationshipType(
            label="ASSERTED_ABOUT_TARGET", description="The statement concerns this target"
        ),
        RelationshipType(
            label="ASSERTED_ABOUT_POPULATION",
            description="The statement concerns this population",
        ),
        RelationshipType(
            label="ASSERTED_ABOUT_FINANCIAL_PROJECTION",
            description="The statement concerns this figure",
        ),
        RelationshipType(
            label="ASSERTED_ABOUT_REGULATORY_EVENT",
            description="The statement concerns this regulatory milestone",
        ),
        RelationshipType(
            label="ASSERTED_ABOUT_ADVERSE_EVENT",
            description="The statement concerns this safety finding",
        ),
        # What an abbreviation stands for.
        RelationshipType(label="HAS_FULL_FORM", description="Expands to a concept"),
        RelationshipType(label="HAS_FULL_FORM_DISEASE", description="Expands to an indication"),
        RelationshipType(label="HAS_FULL_FORM_TARGET", description="Expands to a target"),
        RelationshipType(label="HAS_FULL_FORM_ORGANIZATION", description="Expands to a company"),
        RelationshipType(label="HAS_FULL_FORM_DRUG", description="Expands to a drug"),
        RelationshipType(
            label="HAS_FULL_FORM_ADVERSE_EVENT", description="Expands to a safety finding"
        ),
        RelationshipType(label="HAS_FULL_FORM_GENE", description="Expands to a gene"),
        RelationshipType(label="HAS_FULL_FORM_PROTEIN", description="Expands to a protein"),
        RelationshipType(
            label="HAS_FULL_FORM_REGULATORY_EVENT",
            description="Expands to a regulatory milestone",
        ),
    ],
    patterns=[
        # The business around the molecule.
        ("Organization", "DEVELOPS", "Drug"),
        ("Organization", "CO_DEVELOPS", "Drug"),
        ("Organization", "LICENSES", "Drug"),
        ("Organization", "CONDUCTS", "Study"),
        ("Organization", "PARTNERS_WITH", "Organization"),
        ("Organization", "ACQUIRED", "Organization"),
        # The statement and what it is about.
        ("Evidence", "ASSERTED_ABOUT_DRUG", "Drug"),
        ("Evidence", "ASSERTED_ABOUT_DISEASE", "Disease"),
        ("Evidence", "ASSERTED_ABOUT_STUDY", "Study"),
        ("Evidence", "ASSERTED_ABOUT_TARGET", "Target"),
        ("Evidence", "ASSERTED_ABOUT_POPULATION", "Population"),
        ("Evidence", "ASSERTED_ABOUT_FINANCIAL_PROJECTION", "FinancialProjection"),
        ("Evidence", "ASSERTED_ABOUT_REGULATORY_EVENT", "RegulatoryEvent"),
        ("Evidence", "ASSERTED_ABOUT_ADVERSE_EVENT", "AdverseEvent"),
        # The vocabulary.
        ("Abbreviation", "HAS_FULL_FORM", "Concept"),
        ("Abbreviation", "HAS_FULL_FORM_DISEASE", "Disease"),
        ("Abbreviation", "HAS_FULL_FORM_TARGET", "Target"),
        ("Abbreviation", "HAS_FULL_FORM_ORGANIZATION", "Organization"),
        ("Abbreviation", "HAS_FULL_FORM_DRUG", "Drug"),
        ("Abbreviation", "HAS_FULL_FORM_ADVERSE_EVENT", "AdverseEvent"),
        ("Abbreviation", "HAS_FULL_FORM_GENE", "Gene"),
        ("Abbreviation", "HAS_FULL_FORM_PROTEIN", "Protein"),
        ("Abbreviation", "HAS_FULL_FORM_REGULATORY_EVENT", "RegulatoryEvent"),
    ],
    # Hold the extractor to the labels the graph already uses. Left to itself
    # it invents "Indication" next to Disease and "Trial" next to Study, and
    # the grouping — along with every saved query — stops covering the graph.
    additional_node_types=False,
    additional_relationship_types=False,
    additional_patterns=False,
)

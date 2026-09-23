"""Turn a folder of PDFs into the Markdown the ingest pipeline reads well.

`SimpleKGPipeline` reads a PDF with pypdf, which returns whatever text layer
the file carries. On a corpus of archival scans that is the wrong tool three
ways at once: a scan with no text layer ingests to nothing, a scan whose text
layer is a bad OCR pass ingests to noise, and a 250MB file with a good text
layer is re-parsed on every run. Document Intelligence, which built the graph
this project adopted, went round the problem the same way this module does —
OCR to Markdown first, then ingest the Markdown — and the five source files it
left in the graph carry exactly that provenance header.

So this is a corpus step, not an ingest step:

    graphrag-prepare ~/Downloads/us-ufo-docs            # -> the project's data dir
    graphrag-prepare one.pdf two.pdf --out somewhere/   # explicit files
    graphrag-ingest --skip-ingested                     # then ingest what is new

Per page, not per file. A released case file is routinely a mix: typed pages
with a clean text layer, photostat negatives with none, and pages where a
previous OCR pass produced a character salad that scores as text but reads as
nothing. Each page's text layer is graded; a page that fails is rendered and
OCR'd, and the better of the two readings is kept. The header on each Markdown
file says how many pages went which way, so a graph built from it can say how
much of a document was read rather than recognised.

Two gates decide whether a reading is text at all. The first is shape: the
share of tokens that look like words or numbers. The second is a word list,
because OCR of halftone noise passes the shape test — it comes back as short
pseudo-words, `ee bd ane Cee vere Ser`, at 0.8 on shape and nothing on meaning.
A page that fails both readings is recorded as illegible rather than fed to the
extractor, which would otherwise mint an Agency called "Ser" from it. The price
is that a page of pure abbreviations — a distribution list of unit designators,
a table of booster names — can be judged noise too. `--regrade` applies the
word-list gate to Markdown that was prepared before it existed.

OCR is Tesseract, called as a subprocess. It is not a Python dependency of this
project because it is not a Python package: install it (winget/apt/brew) and
either put it on PATH or set TESSERACT_CMD. Rendering is pypdfium2 and Pillow,
the `ocr` extra: `uv sync --extra ocr`.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

#: What a page's text layer has to score to be trusted without OCR. The score is
#: the share of whitespace-separated tokens that look like words or numbers; a
#: good typed page scores 0.85-0.95, a photostat's garbage layer 0.1-0.3.
TEXT_LAYER_MIN_QUALITY = 0.6
#: ...and how many word-like tokens it needs. A caption under a photograph is a
#: valid text layer and a poor reason not to OCR the rest of the page.
TEXT_LAYER_MIN_WORDS = 25

#: Below this an OCR reading is noise from a photograph or a blank page, and the
#: page is recorded as illegible rather than fed to the extractor as text.
OCR_MIN_QUALITY = 0.5
OCR_MIN_WORDS = 15

#: 200 dpi is Tesseract's sweet spot for typewriter faces. 300 doubles the
#: pixels for no measurable gain on these scans and makes the slow pages slower.
RENDER_DPI = 200
#: A page whose mean luminance is below this is a photographic negative — white
#: type on a dark ground, common in the FBI and Air Force photostats — and is
#: inverted before OCR. Tesseract assumes dark ink on light paper.
NEGATIVE_MEAN_LUMINANCE = 110
#: Page segmentation mode 6, "a single uniform block of text". The automatic
#: mode (3) reads forms slightly better when it works and takes six minutes on
#: a page of halftone noise when it does not; mode 6 is never slower than 15s.
TESSERACT_PSM = "6"
#: Sauvola thresholding (method 2) is local; Tesseract's default, Otsu, is
#: global and finds no ink at all on a grey, unevenly lit photostat.
TESSERACT_THRESHOLDING = "2"
#: Hard ceiling per page. Tesseract is deterministic and a page that has not
#: finished in this long is a page of noise.
OCR_PAGE_TIMEOUT_S = 120

#: Share of a page's longer alphabetic tokens that have to be real words. The
#: shape test above is fooled by OCR run on halftone noise, which comes back as
#: plausible-looking short "words" — `ee bd ane Cee vere Ser` — and scores 0.8
#: on shape while reading as nothing. Against a word list, a typed page scores
#: 0.8-1.0, a form or table 0.6-0.8, and noise 0.2-0.5.
DICTIONARY_MIN_HIT = 0.55
#: Pages with fewer judgeable words than this are not held to the dictionary:
#: a stamp and a serial number is a legitimate page with nothing to look up.
DICTIONARY_MIN_WORDS = 8

WORD = re.compile(r"[A-Za-z]{2,}[.,;:'\"!?)]*")
NUMBER = re.compile(r"[\d.,/:\-]+")
ALPHA_RUN = re.compile(r"[A-Za-z]{3,}")

#: Distilled from the trustworthy text layers of a mixed archival corpus: every
#: alphabetic word of three letters or more seen three times across two or more
#: documents. Ordinary English dominates it, so any English page scores high;
#: it is deliberately not a full dictionary, in which three-letter OCR noise
#: finds a match too often.
WORDLIST_PATH = Path(__file__).with_name("english-words.txt")
_WORDS: set[str] | None = None


def word_list() -> set[str]:
    global _WORDS
    if _WORDS is None:
        _WORDS = set(WORDLIST_PATH.read_text(encoding="utf-8").split())
    return _WORDS


def text_quality(text: str) -> tuple[float, int]:
    """(share of tokens that read as words or numbers, number of word tokens)."""
    tokens = text.split()
    if not tokens:
        return 0.0, 0
    words = sum(1 for tok in tokens if WORD.fullmatch(tok))
    numbers = sum(1 for tok in tokens if NUMBER.fullmatch(tok))
    return (words + numbers) / len(tokens), words


def dictionary_hit_rate(text: str) -> tuple[float, int]:
    """(share of 3+ letter alphabetic runs that are words, how many were judged)."""
    runs = [run.lower() for run in ALPHA_RUN.findall(text)]
    if not runs:
        return 0.0, 0
    words = word_list()
    return sum(1 for run in runs if run in words) / len(runs), len(runs)


def legible(text: str) -> bool:
    """Whether a page's text reads as language rather than as noise shaped like it."""
    hit, judged = dictionary_hit_rate(text)
    return judged < DICTIONARY_MIN_WORDS or hit >= DICTIONARY_MIN_HIT


def find_tesseract() -> str | None:
    """The Tesseract binary: TESSERACT_CMD, then PATH, then the Windows default."""
    configured = os.getenv("TESSERACT_CMD")
    if configured and Path(configured).is_file():
        return configured
    on_path = shutil.which("tesseract")
    if on_path:
        return on_path
    for candidate in (
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Tesseract-OCR/tesseract.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Tesseract-OCR/tesseract.exe",
    ):
        if candidate.is_file():
            return str(candidate)
    return None


@dataclass
class PageReading:
    number: int  # 1-based
    text: str
    method: str  # "text" | "ocr" | "illegible"
    quality: float


@dataclass
class Prepared:
    source: Path
    output: Path
    pages: list[PageReading] = field(default_factory=list)
    seconds: float = 0.0
    error: str | None = None

    def count(self, method: str) -> int:
        return sum(1 for p in self.pages if p.method == method)


def ocr_page(page, tesseract: str, workdir: Path) -> str:
    """Render one pypdfium2 page and read it with Tesseract."""
    from PIL import ImageOps, ImageStat

    image = page.render(scale=RENDER_DPI / 72).to_pil().convert("L")
    if ImageStat.Stat(image).mean[0] < NEGATIVE_MEAN_LUMINANCE:
        image = ImageOps.invert(image)
    # A 1% cutoff stretches the page's actual ink/paper range to full contrast
    # without letting a single specular hole-punch highlight define white.
    image = ImageOps.autocontrast(image, cutoff=1)
    png = workdir / f"page-{os.getpid()}.png"
    image.save(png)
    try:
        result = subprocess.run(
            [
                tesseract,
                str(png),
                "stdout",
                "-l",
                "eng",
                "--dpi",
                str(RENDER_DPI),
                "--psm",
                TESSERACT_PSM,
                "-c",
                f"thresholding_method={TESSERACT_THRESHOLDING}",
            ],
            capture_output=True,
            timeout=OCR_PAGE_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        return ""
    return result.stdout.decode("utf-8", errors="replace")


def tidy(text: str) -> str:
    """Collapse the whitespace scans produce without touching the words."""
    lines = [" ".join(line.split()) for line in text.splitlines()]
    out: list[str] = []
    blank = False
    for line in lines:
        if line:
            out.append(line)
            blank = False
        elif not blank:
            out.append("")
            blank = True
    return "\n".join(out).strip()


def read_pdf(source: Path, tesseract: str | None, force_ocr: bool = False) -> list[PageReading]:
    """Read every page: the text layer where it is trustworthy, OCR otherwise."""
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(source))
    readings: list[PageReading] = []
    with tempfile.TemporaryDirectory(prefix="graphrag-ocr-") as tmp:
        workdir = Path(tmp)
        for index in range(len(pdf)):
            page = pdf[index]
            layer = ""
            if not force_ocr:
                try:
                    layer = page.get_textpage().get_text_range()
                except Exception:  # noqa: BLE001 - a broken text layer is just an absent one
                    layer = ""
            layer_q, layer_words = text_quality(layer)
            if (
                layer_q >= TEXT_LAYER_MIN_QUALITY
                and layer_words >= TEXT_LAYER_MIN_WORDS
                and legible(layer)
            ):
                readings.append(PageReading(index + 1, tidy(layer), "text", layer_q))
                continue

            recognised = ocr_page(page, tesseract, workdir) if tesseract else ""
            ocr_q, ocr_words = text_quality(recognised)
            ocr_ok = ocr_q >= OCR_MIN_QUALITY and ocr_words >= OCR_MIN_WORDS and legible(recognised)
            layer_ok = (
                layer_q >= OCR_MIN_QUALITY and layer_words >= OCR_MIN_WORDS and legible(layer)
            )
            # Keep whichever reading is more legible. A page can have a thin but
            # real text layer (a caption) and an OCR pass that reads nothing.
            if ocr_ok and ocr_words >= layer_words:
                readings.append(PageReading(index + 1, tidy(recognised), "ocr", ocr_q))
            elif layer_ok:
                readings.append(PageReading(index + 1, tidy(layer), "text", layer_q))
            else:
                readings.append(PageReading(index + 1, "", "illegible", max(layer_q, ocr_q)))
    return readings


def render_markdown(source: Path, pages: list[PageReading], tesseract: str | None) -> str:
    """The Markdown the pipeline ingests. Same header shape as Document
    Intelligence wrote for the files already in the graph, so a `source` on a
    Document node reads the same whichever tool produced it."""
    text_pages = sum(1 for p in pages if p.method == "text")
    ocr_pages = sum(1 for p in pages if p.method == "ocr")
    illegible = sum(1 for p in pages if p.method == "illegible")
    engine = "pypdfium2 text layer"
    if ocr_pages:
        engine += " + Tesseract OCR"
    head = [
        f"# Historical Document: {source.stem}",
        "",
        "## Source Metadata",
        "",
        f"- Original file: `{source.name}`",
        f"- Pages: {len(pages)} ({text_pages} from text layer, {ocr_pages} OCR, "
        f"{illegible} illegible)",
        "- OCR language: `eng`",
        f"- Processed at: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Processing pipeline: `{engine} → Markdown → neo4j-graphrag SimpleKGPipeline`",
        "",
        "## Text",
        "",
    ]
    body: list[str] = []
    for page in pages:
        body.append(page_marker(page))
        if page.method != "illegible":
            body.append(page.text)
        body.append("")
    return "\n".join(head + body).rstrip() + "\n"


def page_marker(page: PageReading) -> str:
    """`[Page 12]`, `[Page 12 (OCR)]` or `[Page 12: illegible]` — the method
    travels with the page so a later regrade can keep the header's tally right."""
    if page.method == "illegible":
        return f"[Page {page.number}: illegible]"
    if page.method == "ocr":
        return f"[Page {page.number} (OCR)]"
    return f"[Page {page.number}]"


PAGE_MARKER = re.compile(r"^\[Page (\d+)(?: \((OCR)\))?(: illegible)?\]\n?", re.MULTILINE)
PAGES_LINE = re.compile(r"^- Pages: .*$", re.MULTILINE)


def regrade_markdown(path: Path) -> int:
    """Re-grade a prepared file's pages against the dictionary; return how many
    were demoted to illegible.

    Exists because the dictionary test arrived after a corpus had been prepared,
    and re-OCR-ing thousands of pages to apply a cheap text test is waste. The
    file's own pages are the input; the PDF is not needed.

    Files written before markers carried the method say `[Page N]` for OCR pages
    too. Their header tally is corrected on the assumption that the demoted
    pages were OCR pages — which is what noise almost always is — taking from
    the OCR count first and the text-layer count only when that runs out.
    """
    original = path.read_text(encoding="utf-8")
    head, sep, body = original.partition("\n## Text\n")
    if not sep:
        return 0
    parts = PAGE_MARKER.split(body)
    # split() yields: leading text, then (number, ocr, illegible, content) per page
    rebuilt = [parts[0]]
    counts = {"text": 0, "ocr": 0, "illegible": 0}
    demoted = 0
    for i in range(1, len(parts), 4):
        number, ocr, was_illegible, content = parts[i], parts[i + 1], parts[i + 2], parts[i + 3]
        text = content.strip()
        if was_illegible or not text:
            method = "illegible"
        elif not legible(text):
            method, demoted = "illegible", demoted + 1
        else:
            method = "ocr" if ocr else "text"
        counts[method] += 1
        page = PageReading(int(number), text, method, 0.0)
        rebuilt.append(page_marker(page) + "\n")
        if method != "illegible":
            rebuilt.append(text + "\n")
        rebuilt.append("\n")
    if not demoted:
        return 0

    tally = PAGES_LINE.search(head)
    old_format = "(OCR)]" not in body
    if tally and old_format:
        numbers = [int(n) for n in re.findall(r"\d+", tally.group(0))]
        if len(numbers) == 4:
            _total, text_pages, ocr_pages, illegible = numbers
            from_ocr = min(ocr_pages, demoted)
            counts = {
                "text": text_pages - (demoted - from_ocr),
                "ocr": ocr_pages - from_ocr,
                "illegible": illegible + demoted,
            }
    total = counts["text"] + counts["ocr"] + counts["illegible"]
    new_tally = (
        f"- Pages: {total} ({counts['text']} from text layer, {counts['ocr']} OCR, "
        f"{counts['illegible']} illegible)"
    )
    head = PAGES_LINE.sub(new_tally, head) if tally else head
    path.write_text(head + sep + "".join(rebuilt).rstrip() + "\n", encoding="utf-8")
    return demoted


def prepare_one(source: Path, output: Path, tesseract: str | None, force_ocr: bool) -> Prepared:
    """Worker entry point: one PDF in, one Markdown file out."""
    started = time.monotonic()
    result = Prepared(source=source, output=output)
    try:
        result.pages = read_pdf(source, tesseract, force_ocr)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_markdown(source, result.pages, tesseract), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 - reported per file, the batch goes on
        result.error = f"{type(exc).__name__}: {exc}"
    result.seconds = time.monotonic() - started
    return result


def discover_pdfs(inputs: list[Path]) -> list[Path]:
    found: list[Path] = []
    for item in inputs:
        if item.is_dir():
            found.extend(p for p in item.rglob("*.pdf") if p.is_file())
        elif item.is_file() and item.suffix.lower() == ".pdf":
            found.append(item)
    # Smallest first: most of the corpus lands early and a 250MB scan at the
    # end does not hold the rest hostage.
    return sorted(set(found), key=lambda p: p.stat().st_size)


def main() -> int:
    from graphrag_kit.config import use_utf8_stdout
    from graphrag_kit.project import load_project

    use_utf8_stdout()
    spec = load_project()
    parser = argparse.ArgumentParser(
        description="Convert PDFs to Markdown (text layer or OCR) for graphrag-ingest."
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="PDF files or directories.")
    parser.add_argument(
        "--out",
        type=Path,
        default=spec.data_dir,
        help=f"Where to write the Markdown (default: the project's data dir, {spec.data_dir}).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=max(1, min(6, (os.cpu_count() or 2) - 2)),
        help="Files processed in parallel. OCR is CPU-bound; more than the core count is waste.",
    )
    parser.add_argument(
        "--force", action="store_true", help="Rewrite Markdown that already exists."
    )
    parser.add_argument(
        "--force-ocr", action="store_true", help="OCR every page, ignoring any text layer."
    )
    parser.add_argument(
        "--no-ocr", action="store_true", help="Text layers only; pages without one are illegible."
    )
    parser.add_argument(
        "--regrade",
        action="store_true",
        help=(
            "Inputs are prepared Markdown files (or folders of them): re-grade their pages "
            "against the word list and mark noise pages illegible. No PDF or OCR needed."
        ),
    )
    args = parser.parse_args()

    if args.regrade:
        files: list[Path] = []
        for item in args.inputs:
            files.extend(sorted(item.glob("*.md")) if item.is_dir() else [item])
        changed = 0
        for file in files:
            demoted = regrade_markdown(file)
            if demoted:
                changed += 1
                print(f"regraded {file.name}: {demoted} page(s) now illegible")
        print(f"{len(files)} files checked, {changed} changed")
        return 0

    pdfs = discover_pdfs(args.inputs)
    if not pdfs:
        print("No PDF files found.", file=sys.stderr)
        return 1

    tesseract = None if args.no_ocr else find_tesseract()
    if not args.no_ocr and tesseract is None:
        print(
            "Tesseract not found. Install it and put it on PATH or set TESSERACT_CMD,\n"
            "or pass --no-ocr to use text layers only.",
            file=sys.stderr,
        )
        return 1

    jobs: list[tuple[Path, Path]] = []
    skipped = 0
    for pdf in pdfs:
        target = args.out / f"{pdf.stem}.md"
        if target.exists() and not args.force and target.stat().st_mtime >= pdf.stat().st_mtime:
            skipped += 1
            continue
        jobs.append((pdf, target))

    print(f"project: {spec.key}")
    print(f"ocr:     {tesseract or 'disabled'}")
    print(
        f"{len(pdfs)} PDFs, {skipped} already prepared, {len(jobs)} to do, {args.workers} workers"
    )
    if not jobs:
        return 0

    totals = {"text": 0, "ocr": 0, "illegible": 0}
    failures: list[Prepared] = []
    started = time.monotonic()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(prepare_one, pdf, target, tesseract, args.force_ocr): pdf
            for pdf, target in jobs
        }
        done = 0
        for future in as_completed(futures):
            done += 1
            result = future.result()
            if result.error:
                failures.append(result)
                print(
                    f"[{done}/{len(jobs)}] FAILED {result.source.name}: {result.error}", flush=True
                )
                continue
            for key in totals:
                totals[key] += result.count(key)
            print(
                f"[{done}/{len(jobs)}] {result.source.name}: {len(result.pages)}p "
                f"(text {result.count('text')}, ocr {result.count('ocr')}, "
                f"illegible {result.count('illegible')}) {result.seconds:.0f}s",
                flush=True,
            )

    elapsed = time.monotonic() - started
    print(
        f"\n{len(jobs) - len(failures)} files in {elapsed / 60:.1f} min: "
        f"{totals['text']} pages from text layers, {totals['ocr']} OCR'd, "
        f"{totals['illegible']} illegible."
    )
    if failures:
        print(f"{len(failures)} failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure.source.name}: {failure.error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())


# --- The same reading, inside the pipeline -----------------------------------

try:
    from neo4j_graphrag.components.data_loader import (
        DataLoader,
        DocumentInfo,
        DocumentType,
        LoadedDocument,
        MarkdownLoader,
        PdfLoader,
    )
except ImportError:  # pragma: no cover - neo4j-graphrag is a hard dependency
    DataLoader = object  # type: ignore[assignment,misc]


class PreparedFileLoader(DataLoader):  # type: ignore[misc]
    """The pipeline's file loader, reading PDFs the way `graphrag-prepare` does.

    `SimpleKGPipeline`'s default loader hands a PDF to pypdf and ingests whatever
    text layer comes back — nothing, for a scan. Routing PDFs through
    `read_pdf` instead means a scanned file dropped on the explorer's "Extend
    the graph" gets the same per-page grading and OCR fallback as the batch,
    and the same header, so its `source` looks like every other one.

    Falls back to pypdf when the `ocr` extra is not installed, so the loader
    is safe to use unconditionally. Markdown goes straight through.
    """

    async def run(self, filepath, metadata=None, fs=None) -> LoadedDocument:
        import asyncio

        path = Path(str(filepath))
        if path.suffix.lower() != ".pdf":
            return await MarkdownLoader().run(filepath=str(path), metadata=metadata, fs=fs)
        try:
            import pypdfium2  # noqa: F401
        except ImportError:
            return await PdfLoader().run(filepath=str(path), metadata=metadata, fs=fs)
        tesseract = find_tesseract()
        # CPU-bound and often minutes long on a big scan: keep the event loop free
        # so the explorer can keep streaming progress while it runs.
        pages = await asyncio.to_thread(read_pdf, path, tesseract)
        return LoadedDocument(
            text=render_markdown(path, pages, tesseract),
            document_info=DocumentInfo(
                path=str(path),
                metadata=self.get_document_metadata("", metadata),
                document_type=DocumentType.PDF,
            ),
        )

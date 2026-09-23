"""The page grader in graphrag-prepare: what counts as a readable text layer.

The decision it makes is whether to trust a PDF's own text or pay for OCR, so
the cases worth pinning are the two kinds of page that fooled a per-file
heuristic: a scan whose text layer is character salad, and a photograph whose
only text is a caption.
"""

from __future__ import annotations

from pathlib import Path

from graphrag_kit.prepare import (
    OCR_MIN_QUALITY,
    TEXT_LAYER_MIN_QUALITY,
    TEXT_LAYER_MIN_WORDS,
    PageReading,
    render_markdown,
    text_quality,
    tidy,
)

TYPED_PAGE = (
    "CHECK-LIST - UNIDENTIFIED FLYING OBJECTS. 1. Date 8 July 47. 2. Time 10:00. "
    "3. Location Muroc Army Air Field, Muroc, Calif. 4. Name of observer Jennette "
    "Marie Scott. 5. Occupation of observer Secretary to 1st Lt J. C. McHenry. "
    "8. Number of objects 3 - two the first time - 1 later. 11. Altitude Approx 8,000 ft. "
    "12. Speed 300 to 400 MPH. 13. Direction of flight Northwest - toward Mojave, Calif."
)

# Verbatim from the text layer of an FBI photostat: what a bad OCR pass leaves.
GARBAGE_LAYER = (
    r"..., ) .) ,. . b ,. I l .. 0 .., t:> 4 -&~~~ ~ ~ ..,;. ~ ~- ~ _..,,.. :I)~ ul "
    r"\.t.- \"r'~\"\" 9- t.> ~ ~ - -~ ~ >~ $,. ~ ..~<S ~., ~--~ '<\ \" ~ 8.l 'N011'\"3 "
    r"C'f~ ... ~~ lS, HVi(l,a tt'~0N ~ ~)\ NJ :U :i -(] ,'.j3ij Jt.t : I.., , ( .)"
)


def test_a_typed_page_is_trusted_without_ocr():
    quality, words = text_quality(TYPED_PAGE)
    assert quality >= TEXT_LAYER_MIN_QUALITY
    assert words >= TEXT_LAYER_MIN_WORDS


def test_a_garbage_text_layer_is_sent_to_ocr():
    quality, words = text_quality(GARBAGE_LAYER)
    assert quality < TEXT_LAYER_MIN_QUALITY
    # ...and is not good enough to keep even as the fallback reading.
    assert quality < OCR_MIN_QUALITY or words < TEXT_LAYER_MIN_WORDS


def test_a_caption_alone_does_not_excuse_the_rest_of_the_page():
    quality, words = text_quality("Figure 3. Object photographed over Oak Ridge.")
    assert quality >= TEXT_LAYER_MIN_QUALITY
    assert words < TEXT_LAYER_MIN_WORDS


def test_empty_text_scores_zero():
    assert text_quality("") == (0.0, 0)
    assert text_quality("   \n\n ") == (0.0, 0)


def test_tidy_collapses_scan_whitespace_but_keeps_lines():
    assert tidy("a   b\n\n\n\nc  \n") == "a b\n\nc"


def test_markdown_carries_the_page_tally_and_marks_illegible_pages():
    pages = [
        PageReading(1, "Read from the text layer.", "text", 0.9),
        PageReading(2, "Recognised by OCR.", "ocr", 0.7),
        PageReading(3, "", "illegible", 0.1),
    ]
    md = render_markdown(Path("Case-File.pdf"), pages, tesseract="tesseract")
    assert md.startswith("# Historical Document: Case-File")
    assert "- Original file: `Case-File.pdf`" in md
    assert "Pages: 3 (1 from text layer, 1 OCR, 1 illegible)" in md
    assert "[Page 3: illegible]" in md
    # The header, not the body, says OCR was involved.
    assert "Tesseract OCR" in md.split("## Text")[0]


NOISE_PAGE = (
    "ee bd a ane Cee ea vere gM rt. Ser us SAR Pts ea os as aoe pth S, Mayres tueere ae "
    "ue out Bes he) Bele cdet BLA are eee =e i aie ark rae oo CS eae <a aa Va yt yao Lene "
    "ay, te Maen srr se te hegebl a Merete Mi ie a em eee cc amen eae ae Me aN ae"
)


def test_ocr_noise_shaped_like_words_fails_the_dictionary():
    from graphrag_kit.prepare import legible, text_quality

    quality, words = text_quality(NOISE_PAGE)
    # This is exactly the page the shape test waved through...
    assert quality >= 0.6 and words >= 15
    # ...and the dictionary does not.
    assert not legible(NOISE_PAGE)


def test_a_typed_page_and_a_table_are_legible():
    from graphrag_kit.prepare import legible

    assert legible(TYPED_PAGE)
    assert legible(
        "LAUNCH FACILITY GUIDE BLDG PRESENT FORMER BLDG PRESENT FORMER NUMBER DESIGNATION "
        "VEHICLE TYPE PROGRAM BOOSTER COMMAND SEQUENCE DATE NICKNAME FACILITY"
    )


def test_too_few_words_to_judge_is_not_held_against_a_page():
    from graphrag_kit.prepare import legible

    assert legible("SECRET 1.4(a) 62-83894-153 ENCLOSURE")


def test_regrade_demotes_noise_pages_and_fixes_the_tally(tmp_path):
    from graphrag_kit.prepare import regrade_markdown

    pages = [
        PageReading(1, TYPED_PAGE, "text", 0.9),
        PageReading(2, NOISE_PAGE, "ocr", 0.8),
        PageReading(3, "", "illegible", 0.1),
    ]
    file = tmp_path / "Case.md"
    file.write_text(render_markdown(Path("Case.pdf"), pages, "tesseract"), encoding="utf-8")
    assert regrade_markdown(file) == 1
    text = file.read_text(encoding="utf-8")
    assert "Pages: 3 (1 from text layer, 0 OCR, 2 illegible)" in text
    assert "[Page 2: illegible]" in text
    assert NOISE_PAGE.split()[0] + " " + NOISE_PAGE.split()[1] not in text
    assert "[Page 1]" in text and TYPED_PAGE[:30] in text
    # Idempotent: a second pass changes nothing.
    assert regrade_markdown(file) == 0


def test_regrade_handles_files_written_before_markers_carried_the_method(tmp_path):
    from graphrag_kit.prepare import regrade_markdown

    old_style = (
        "# Historical Document: Old\n\n## Source Metadata\n\n- Original file: `Old.pdf`\n"
        "- Pages: 2 (1 from text layer, 1 OCR, 0 illegible)\n\n## Text\n\n"
        f"[Page 1]\n{TYPED_PAGE}\n\n[Page 2]\n{NOISE_PAGE}\n"
    )
    file = tmp_path / "Old.md"
    file.write_text(old_style, encoding="utf-8")
    assert regrade_markdown(file) == 1
    text = file.read_text(encoding="utf-8")
    # The demoted page is assumed to have been the OCR one.
    assert "Pages: 2 (1 from text layer, 0 OCR, 1 illegible)" in text
    assert "[Page 2: illegible]" in text

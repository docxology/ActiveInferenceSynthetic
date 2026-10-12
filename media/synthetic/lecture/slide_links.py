"""Attach working publication and repository links to the rendered slide PDF."""

from __future__ import annotations

import json
from pathlib import Path

__all__ = ["link_slides"]


def link_slides(source: Path, target: Path, project: Path) -> dict[str, object]:
    """Preserve the rendered pages and add URI annotations in their visible text areas."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.annotations import Link

    publication = json.loads((project / "publication.json").read_text())
    reader = PdfReader(source)
    if len(reader.pages) != 26 or target.exists():
        raise ValueError("Expected 26 untouched slide pages and a fresh linked-PDF target")
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    records = []

    def add(page_index: int, url: str, box: tuple[int, int, int, int]) -> None:
        page = writer.pages[page_index]
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        x0, y0, x1, y1 = box
        rect = (
            x0 * width / 1920,
            (1080 - y1) * height / 1080,
            x1 * width / 1920,
            (1080 - y0) * height / 1080,
        )
        writer.add_annotation(page_index, Link(rect=rect, url=url))
        records.append({"page": page_index + 1, "url": url, "pixel_box": list(box)})

    for index, link in enumerate(publication["links"][:2]):
        y = 600 + index * 210
        add(0, link["url"], (948, y, 1830, y + 164))
    repositories = [
        "fep_formal",
        "Generalized_Notation_Notation",
        "Active_Inference_Ontology",
        "fundamentals",
        "courses",
        "cognitive",
        "ActiveInferenceJournal",
    ]
    for index, name in enumerate(repositories):
        y = 333 + index * 74
        add(25, "https://github.com/ActiveInferenceInstitute/" + name, (98, y, 1230, y + 53))
    for page_index in range(1, 26):
        add(page_index, publication["links"][0]["url"], (64, 1020, 1275, 1060))
    add(25, publication["links"][2]["url"], (1360, 674, 1830, 830))
    with target.open("xb") as stream:
        writer.write(stream)
    reopened = PdfReader(target)
    actual = [
        str(annotation.get_object()["/A"]["/URI"])
        for page in reopened.pages
        for annotation in page.get("/Annots", [])
        if annotation.get_object().get("/A", {}).get("/S") == "/URI"
    ]
    if sorted(actual) != sorted(record["url"] for record in records):
        raise ValueError("Linked-PDF annotation round-trip differs from the declared links")
    return {"pages": len(reopened.pages), "links": records, "roundtrip_exact": True}

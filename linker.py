import pymupdf

from toc import TocEntry, detect_page_offset, extract_entries, find_toc_pages, get_all_entries


def add_link(page, entry: TocEntry, offset: int):
    target = entry.page - 1 + offset

    if target < 0 or target >= len(page.parent):
        return

    page.insert_link({
        "kind": pymupdf.LINK_GOTO,
        "from": pymupdf.Rect(entry.bbox),
        "page": target,
    })


def add_links(page, entries, offset: int):
    for entry in entries:
        add_link(page, entry, offset)


def convert_pdf(input_path: str, output_path: str, mode: str = "mid"):
    if mode == "low":
        dpi = 150
        max_toc_pages = 25
        offset_pages = 40

    elif mode == "high":
        dpi = 300
        max_toc_pages = 30
        offset_pages = 120

    else:
        dpi = 220
        max_toc_pages = 25
        offset_pages = 80

    doc = pymupdf.open(input_path)

    try:
        toc_pages = find_toc_pages(doc, max_pages=max_toc_pages, dpi=dpi)

        if not toc_pages:
            raise ValueError("Table of contents not found.")

        all_entries = get_all_entries(doc, toc_pages, dpi=dpi)

        if not all_entries:
            raise ValueError("No TOC entries found.")

        offset = detect_page_offset(doc, max_pages=offset_pages, dpi=dpi)

        if offset is None:
            raise ValueError("Could not detect page offset.")

        for page_idx in toc_pages:
            page = doc[page_idx]
            entries = extract_entries(page, dpi=dpi)
            add_links(page, entries, offset)

        doc.save(output_path)

    finally:
        doc.close()
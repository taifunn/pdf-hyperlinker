import re
from dataclasses import dataclass

from pdf_text import TextLine, get_page_lines


@dataclass
class TocEntry:
    title: str
    page: int
    bbox: tuple[float, float, float, float]


def parse_line(line: TextLine) -> TocEntry | None:
    parts = line.text.strip().split()

    if len(parts) < 2:
        return None

    page = None
    page_index = None

    for i in range(len(parts) - 1, -1, -1):
        cleaned = parts[i].strip(" .,-:;[]()")

        if cleaned.isdigit():
            page = int(cleaned)
            page_index = i
            break

    if page is None:
        return None

    title = " ".join(parts[:page_index]).strip(" .,-:;")

    if not title:
        return None

    return TocEntry(
        title=title,
        page=page,
        bbox=line.bbox,
    )


def _is_page_number(text: str) -> bool:
    return bool(re.fullmatch(r"\d{1,4}", text.strip()))


def _merge_lines(first: TextLine, second: TextLine) -> TextLine:
    return TextLine(
        text=f"{first.text} {second.text}",
        bbox=(
            min(first.bbox[0], second.bbox[0]),
            min(first.bbox[1], second.bbox[1]),
            max(first.bbox[2], second.bbox[2]),
            max(first.bbox[3], second.bbox[3]),
        ),
    )


def extract_entries(page, dpi: int = 300):
    entries = []
    lines = get_page_lines(page, dpi=dpi)
    index = 0

    while index < len(lines):
        line = lines[index]

        if line.text.strip().lower() in {
            "contents",
            "table of contents",
            "spis treści",
            "spis tresci",
        }:
            index += 1
            continue

        if (
            index + 1 < len(lines)
            and not _is_page_number(line.text)
            and _is_page_number(lines[index + 1].text)
        ):
            line = _merge_lines(line, lines[index + 1])
            index += 1

        entry = parse_line(line)

        if entry is not None:
            entries.append(entry)

        index += 1

    return entries

def is_toc_page(page, dpi: int = 300):
    lines = get_page_lines(page, dpi=dpi)

    if not lines:
        return False

    headings = {
        "contents",
        "table of contents",
        "spis treści",
        "spis tresci",
    }

    if any(line.text.strip().lower() in headings for line in lines):
        return True

    if len(extract_entries(page, dpi=dpi)) >= 20:
        return True

    return False

def find_toc_pages(doc, max_pages: int = 20, dpi: int = 300):
    toc_pages = []

    for page_idx in range(min(max_pages, len(doc))):
        if is_toc_page(doc[page_idx], dpi=dpi):
            toc_pages.append(page_idx)

    if not toc_pages:
        return []

    runs = []
    current_run = [toc_pages[0]]

    for page_idx in toc_pages[1:]:
        if page_idx == current_run[-1] + 1:
            current_run.append(page_idx)
        else:
            runs.append(current_run)
            current_run = [page_idx]

    runs.append(current_run)
    return max(runs, key=len)


def get_all_entries(doc, toc_pages, dpi: int = 300):
    entries = []

    for page_idx in toc_pages:
        entries.extend(extract_entries(doc[page_idx], dpi=dpi))

    return entries


def get_printed_page_number(page, dpi: int = 300):
    lines = get_page_lines(page, dpi=dpi)
    height = page.rect.height

    for line in lines:
        y0 = line.bbox[1]
        y1 = line.bbox[3]

        near_top = y1 < height * 0.25
        near_bottom = y0 > height * 0.75

        if not near_top and not near_bottom:
            continue

        match = re.search(r"\b(\d{1,4})\b", line.text)

        if match:
            return int(match.group(1))

    return None


def detect_page_offset(doc, max_pages: int = 80, dpi: int = 300):
    offsets = []

    for page_idx in range(min(max_pages, len(doc))):
        printed_page = get_printed_page_number(doc[page_idx], dpi=dpi)

        if printed_page is None:
            continue

        offset = page_idx - (printed_page - 1)
        offsets.append(offset)

    if not offsets:
        return None

    return max(set(offsets), key=offsets.count)
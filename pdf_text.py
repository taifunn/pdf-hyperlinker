import io
from dataclasses import dataclass

import pytesseract
from PIL import Image


@dataclass
class TextLine:
    text: str
    bbox: tuple[float, float, float, float]


_cache = {}


def get_text_lines(page):
    data = page.get_text("dict")
    result = []

    for block in data.get("blocks", []):
        if block.get("type") != 0:
            continue

        for line in block.get("lines", []):
            text = " ".join(span.get("text", "").strip() for span in line.get("spans", []))
            text = text.strip()

            if not text:
                continue

            result.append(TextLine(text=text, bbox=tuple(line["bbox"])))

    return result


def has_text(page, min_chars: int = 20):
    return len(page.get_text("text").strip()) >= min_chars


def get_ocr_lines(page, dpi: int = 300):
    pix = page.get_pixmap(dpi=dpi)

    scale_x = page.rect.width / pix.width
    scale_y = page.rect.height / pix.height

    image = Image.open(io.BytesIO(pix.tobytes("png")))

    data = pytesseract.image_to_data(
        image,
        lang="pol+eng",
        config="--psm 6",
        output_type=pytesseract.Output.DICT,
    )

    words = []

    for i, text in enumerate(data["text"]):
        text = text.strip()

        if not text:
            continue

        left = data["left"][i]
        top = data["top"][i]
        width = data["width"][i]
        height = data["height"][i]

        words.append({
            "text": text,
            "left": left,
            "top": top,
            "width": width,
            "height": height,
            "y": top + height / 2,
        })

    words.sort(key=lambda word: (word["y"], word["left"]))

    lines = []

    for word in words:
        found = None

        for line in lines:
            tolerance = max(8, word["height"] * 0.7)

            if abs(line["y"] - word["y"]) <= tolerance:
                found = line
                break

        if found is None:
            lines.append({
                "y": word["y"],
                "words": [word],
            })
        else:
            found["words"].append(word)
            found["y"] = sum(w["y"] for w in found["words"]) / len(found["words"])

    result = []

    for line in lines:
        line_words = sorted(line["words"], key=lambda word: word["left"])

        x0 = min(word["left"] for word in line_words)
        y0 = min(word["top"] for word in line_words)
        x1 = max(word["left"] + word["width"] for word in line_words)
        y1 = max(word["top"] + word["height"] for word in line_words)

        text = " ".join(word["text"] for word in line_words)

        bbox = (
            x0 * scale_x,
            y0 * scale_y,
            x1 * scale_x,
            y1 * scale_y,
        )

        result.append(TextLine(text=text, bbox=bbox))

    result.sort(key=lambda line: line.bbox[1])

    return result


def get_page_lines(page, dpi: int = 300):
    key = (id(page.parent), page.number, dpi)

    if key in _cache:
        return _cache[key]

    if has_text(page):
        lines = get_text_lines(page)
    else:
        lines = get_ocr_lines(page, dpi=dpi)

    _cache[key] = lines

    return lines
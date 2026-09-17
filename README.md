# PDF Hyperlinker

A simple Python tool that adds clickable links to a PDF table of contents.

## Features

- Detects table of contents pages
- Supports text-based and scanned PDFs
- Uses OCR for scanned pages
- Automatically detects page number offset
- Supports `low`, `mid`, and `high` modes

## Requirements

- Python 3.10+
- Tesseract OCR

On macOS:

```bash
brew install tesseract
```

## Installation

Clone the repository:

```bash
git clone https://github.com/taifunn/pdf-hyperlinker.git
cd pdf-hyperlinker
```

Install `pipx`:

```bash
brew install pipx
pipx ensurepath
```

Install PDF Hyperlinker:

```bash
pipx install .
```

## Usage

Basic usage:

```bash
pdf-hyperlinker book.pdf
```

You can use any file path:

```bash
pdf-hyperlinker ~/Downloads/book.pdf
```

Choose a mode:

```bash
pdf-hyperlinker book.pdf -m low
pdf-hyperlinker book.pdf -m mid
pdf-hyperlinker book.pdf -m high
```

Choose the output file:

```bash
pdf-hyperlinker book.pdf -o result.pdf
```

If no output file is provided, the result is saved next to the original file as:

```text
book_linked.pdf
```

## Modes

- `low` — faster
- `mid` — balanced, default
- `high` — more accurate

## Project Structure

```text
pdf-hyperlinker/
├── cli.py
├── linker.py
├── toc.py
├── pdf_text.py
├── pyproject.toml
└── README.md
```
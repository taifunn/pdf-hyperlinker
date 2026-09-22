# PDF Hyperlinker

A simple Python tool that adds clickable links to a PDF table of contents.

## Features

* Detects table of contents pages
* Supports text-based and scanned PDFs
* Uses OCR for scanned pages
* Automatically detects page number offset
* Supports `low`, `mid`, and `high` modes

## Requirements

* Python 3.10+
* Tesseract OCR
* pipx

## Installation

Clone the repository:

```bash
git clone https://github.com/taifunn/pdf-hyperlinker.git
cd pdf-hyperlinker
```

Install `pipx` if it is not already installed.

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
pdf-hyperlinker book.pdf --mode low
pdf-hyperlinker book.pdf --mode mid
pdf-hyperlinker book.pdf --mode high
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

* `low` — faster
* `mid` — balanced, default
* `high` — more accurate

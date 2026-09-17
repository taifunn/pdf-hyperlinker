import argparse
from pathlib import Path

from linker import convert_pdf


def build_parser():
    parser = argparse.ArgumentParser(description="Add clickable links to a PDF table of contents.")

    parser.add_argument("input", help="Input PDF file.")
    parser.add_argument("-o", "--output", help="Output PDF file.")
    parser.add_argument("--mode", choices=["low", "mid", "high"], default="mid")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.is_file():
        parser.error(f"File not found: {input_path}")

    output_path = Path(args.output) if args.output else input_path.with_name(f"{input_path.stem}_linked.pdf")

    try:
        convert_pdf(input_path, output_path, mode=args.mode)
    except Exception as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
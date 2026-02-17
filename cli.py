"""
Command-line interface for PDF Watermark Remover.

Usage:
    python cli.py input.pdf "CONFIDENTIAL" "DRAFT"
    python cli.py input.pdf "Watermark" --method pymupdf --output-dir ./results
    python cli.py input.pdf "Sample" --check-only
"""

import argparse
import sys

from src.pdf_watermark_remover.core import check_watermarks_in_pdf, remove_watermarks_pymupdf
from src.pdf_watermark_remover.redactor import remove_watermarks_redactor
from src.pdf_watermark_remover.utils import make_output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-watermark-remover",
        description="Remove text and image watermarks from PDF files.",
    )
    parser.add_argument("input", help="Path to the input PDF file.")
    parser.add_argument(
        "watermarks",
        nargs="+",
        metavar="WATERMARK",
        help="One or more watermark text strings to remove.",
    )
    parser.add_argument(
        "--method",
        choices=["redactor", "pymupdf"],
        default="redactor",
        help="Removal method: 'redactor' (content-stream, default) or 'pymupdf' (draw/delete).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        metavar="DIR",
        help="Directory for the output file. Defaults to 'output-pdf/' next to the input file.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check for the presence of watermarks; do not modify the file.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # --- Check only ---
    results = check_watermarks_in_pdf(args.input, args.watermarks)
    print("\n🔍 Watermark detection results:")
    for wm, found in results.items():
        status = "✅ FOUND" if found else "❌ NOT FOUND"
        print(f"  {status}: '{wm}'")

    if args.check_only:
        sys.exit(0)

    # --- Remove ---
    output_path = make_output_path(args.input, args.output_dir)
    print(f"\n🗑️  Removing watermarks using method: {args.method} …")

    if args.method == "redactor":
        remove_watermarks_redactor(args.input, output_path, args.watermarks)
    else:
        remove_watermarks_pymupdf(args.input, output_path, args.watermarks)

    print(f"✅ Done! Cleaned file saved to: {output_path}\n")


if __name__ == "__main__":
    main()

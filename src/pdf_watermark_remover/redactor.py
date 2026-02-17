"""
Watermark removal using pdf-redactor library.
Operates at the content-stream level — more thorough than PyMuPDF drawing.
"""

import re
import pdf_redactor


def remove_watermarks_redactor(
    input_pdf_path: str,
    output_pdf_path: str,
    watermark_list: list[str],
) -> None:
    """
    Remove text watermarks using pdf-redactor (content-stream level).

    This method removes text from the PDF content stream itself, making it
    more reliable than drawing white rectangles over the text.

    Args:
        input_pdf_path: Path to the source PDF file.
        output_pdf_path: Path where the cleaned PDF will be saved.
        watermark_list: List of watermark text strings to remove.
    """
    options = pdf_redactor.RedactorOptions()
    options.content_filters = [
        (re.compile(re.escape(wm), re.IGNORECASE), lambda m: "")
        for wm in watermark_list
        if wm.strip()
    ]
    with (
        open(input_pdf_path, "rb") as infile,
        open(output_pdf_path, "wb") as outfile,
    ):
        options.input_stream = infile
        options.output_stream = outfile
        pdf_redactor.redactor(options)

"""
Utility helpers for file path handling and temp file management.
"""

import os
import tempfile


def make_output_path(input_path: str, output_dir: str | None = None) -> str:
    """
    Build an output file path for the cleaned PDF.

    Args:
        input_path: Path to the original PDF.
        output_dir: Directory for the output file. Defaults to an 'output-pdf'
                    folder next to the input file.

    Returns:
        Full path to the output PDF file.
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(input_path)), "output-pdf")
    os.makedirs(output_dir, exist_ok=True)
    filename = f"cleaned_{os.path.basename(input_path)}"
    return os.path.join(output_dir, filename)


def save_uploaded_file(uploaded_bytes: bytes, suffix: str = ".pdf") -> str:
    """
    Save bytes from an uploaded file to a temporary file on disk.

    Args:
        uploaded_bytes: Raw file content.
        suffix: File extension for the temp file.

    Returns:
        Path to the created temporary file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_bytes)
        return tmp.name

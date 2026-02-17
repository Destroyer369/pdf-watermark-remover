"""PDF Watermark Remover — core package."""

from .core import (
    check_watermarks_in_pdf,
    remove_watermarks_pymupdf,
)
from .redactor import remove_watermarks_redactor

__all__ = [
    "check_watermarks_in_pdf",
    "remove_watermarks_pymupdf",
    "remove_watermarks_redactor",
]

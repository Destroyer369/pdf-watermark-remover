"""
Core watermark removal logic using PyMuPDF (fitz).
Shared between CLI and web application.
"""

import fitz  # PyMuPDF


def remove_text_watermark_draw(page: fitz.Page, watermark_text: str) -> None:
    """
    Cover text watermark with a white rectangle (non-destructive approach).

    Args:
        page: PyMuPDF page object.
        watermark_text: The text string to search for and cover.
    """
    text_instances = page.search_for(watermark_text)
    for inst in text_instances:
        page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))


def remove_text_watermark_delete(page: fitz.Page, watermark_text: str) -> None:
    """
    Delete text watermark objects from the page (destructive approach).

    Args:
        page: PyMuPDF page object.
        watermark_text: The text string to search for and delete.
    """
    text_instances = page.search_for(watermark_text)
    for inst in text_instances:
        page.delete_text(watermark_text, clip=inst)


def remove_image_watermarks(page: fitz.Page) -> None:
    """
    Remove image-based watermarks that use a transparency mask (smask).

    Args:
        page: PyMuPDF page object.
    """
    img_list = page.get_images(full=True)
    for img in img_list:
        xref = img[0]
        try:
            smask = page.parent.extract_image(xref).get("smask")
            if smask:
                page._delete_object(xref)
        except Exception:
            pass


def remove_watermarks_pymupdf(
    input_pdf_path: str,
    output_pdf_path: str,
    watermark_list: list[str],
    delete_text: bool = False,
) -> None:
    """
    Remove watermarks from a PDF using PyMuPDF.

    Args:
        input_pdf_path: Path to the source PDF file.
        output_pdf_path: Path where the cleaned PDF will be saved.
        watermark_list: List of watermark text strings to remove.
        delete_text: If True, deletes text objects; otherwise covers with white rectangle.
    """
    doc = fitz.open(input_pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        for wm in watermark_list:
            if wm.strip():
                if delete_text:
                    remove_text_watermark_delete(page, wm)
                else:
                    remove_text_watermark_draw(page, wm)
        remove_image_watermarks(page)
    doc.save(output_pdf_path)
    doc.close()


def check_watermarks_in_pdf(
    pdf_path: str,
    watermark_list: list[str],
) -> dict[str, bool]:
    """
    Check which watermarks are present in a PDF file.

    Args:
        pdf_path: Path to the PDF file.
        watermark_list: List of watermark text strings to search for.

    Returns:
        A dict mapping each watermark text to True (found) or False (not found).
    """
    results: dict[str, bool] = {}
    doc = fitz.open(pdf_path)
    for wm in watermark_list:
        found = False
        for page_num in range(len(doc)):
            if doc[page_num].search_for(wm):
                found = True
                break
        results[wm] = found
    doc.close()
    return results

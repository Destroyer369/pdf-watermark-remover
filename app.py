"""
Streamlit web application for PDF Watermark Remover.

Run with:
    streamlit run app.py
"""

import os
import tempfile

import streamlit as st

from src.pdf_watermark_remover.core import check_watermarks_in_pdf, remove_watermarks_pymupdf
from src.pdf_watermark_remover.redactor import remove_watermarks_redactor
from src.pdf_watermark_remover.utils import save_uploaded_file


def main() -> None:
    st.set_page_config(page_title="PDF Watermark Remover", page_icon="🧹")
    st.title("🧹 PDF Watermark Remover")
    st.markdown("Upload a PDF and specify the watermark text(s) you want to remove.")

    # --- Sidebar: settings ---
    with st.sidebar:
        st.header("⚙️ Settings")
        use_redactor = st.checkbox(
            "Use pdf-redactor (content-stream level removal)",
            value=True,
            help="More thorough — removes text from the content stream. "
                 "Uncheck to use PyMuPDF (draws white rectangles over the text instead).",
        )

    # --- File upload ---
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    # --- Watermark input ---
    watermark_input = st.text_area(
        "Watermark text(s) to remove (one per line)",
        height=120,
        placeholder="CONFIDENTIAL\nDRAFT\nSample watermark text",
    )
    watermark_list = [wm.strip() for wm in watermark_input.splitlines() if wm.strip()]

    if not uploaded_file:
        st.info("Please upload a PDF file to get started.")
        return

    # Save the upload to a temp file once so we can reuse it
    input_pdf_path = save_uploaded_file(uploaded_file.read())

    # --- Check button ---
    if st.button("🔍 Check for watermarks", disabled=not watermark_list):
        results = check_watermarks_in_pdf(input_pdf_path, watermark_list)
        st.subheader("Detection results")
        for wm, found in results.items():
            icon = "✅" if found else "❌"
            st.write(f"{icon} **'{wm}'**: {'Found' if found else 'Not found'}")

    st.divider()

    # --- Remove button ---
    if st.button("🗑️ Remove watermarks & download", disabled=not watermark_list):
        output_pdf_path = os.path.join(
            tempfile.gettempdir(),
            f"cleaned_{os.path.basename(input_pdf_path)}",
        )

        with st.spinner("Processing PDF…"):
            if use_redactor:
                remove_watermarks_redactor(input_pdf_path, output_pdf_path, watermark_list)
            else:
                remove_watermarks_pymupdf(input_pdf_path, output_pdf_path, watermark_list)

        st.success("✅ Watermarks removed successfully!")
        with open(output_pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download cleaned PDF",
                data=f,
                file_name="cleaned_output.pdf",
                mime="application/pdf",
            )


if __name__ == "__main__":
    main()

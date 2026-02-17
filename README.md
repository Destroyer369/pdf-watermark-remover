# 🧹 PDF Watermark Remover

A Python tool to remove **text** and **image-text** watermarks from PDF files.
Available as both a **Streamlit web app** and a **command-line interface (CLI)**.

## ⚖️ Legal Disclaimer

This tool is intended for **legitimate use cases only**, such as:

- Removing watermarks from documents you own or have created
- Processing documents for which you have explicit permission
- Internal/corporate document workflows

The authors are **not responsible** for any misuse of this software.
Users are solely responsible for ensuring their usage complies with
applicable copyright laws and terms of service of any content they process.

## ✨ Features

- Remove text watermarks (single or multiple at once)
- Remove semi-transparent image watermarks (smask-based)
- Two removal strategies:
  - **pdf-redactor** — operates at the content-stream level (more thorough)
  - **PyMuPDF** — draws white rectangles or deletes text objects
- Detect watermarks before removing them
- Web UI via Streamlit
- CLI for batch/script usage

## 📁 Project Structure

```
pdf-watermark-remover/
├── src/
│   └── pdf_watermark_remover/
│       ├── __init__.py       # Public API
│       ├── core.py           # PyMuPDF-based removal logic
│       ├── redactor.py       # pdf-redactor wrapper
│       └── utils.py          # File path helpers
├── tests/
│   ├── __init__.py
│   └── test_core.py          # Unit tests
├── app.py                    # Streamlit web app entry point
├── cli.py                    # CLI entry point
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## 🚀 Installation

```bash
git clone https://github.com/YOUR_USERNAME/pdf-watermark-remover.git
cd pdf-watermark-remover

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## 🖥️ Web App (Streamlit)

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser, upload a PDF, enter the watermark text(s), and click **Remove watermarks & download**.

## ⌨️ CLI Usage

```bash
# Remove a single watermark
python cli.py document.pdf "CONFIDENTIAL"

# Remove multiple watermarks
python cli.py document.pdf "CONFIDENTIAL" "DRAFT" "Sample"

# Check for watermarks without modifying the file
python cli.py document.pdf "CONFIDENTIAL" --check-only

# Use PyMuPDF method instead of pdf-redactor
python cli.py document.pdf "DRAFT" --method pymupdf

# Specify a custom output directory
python cli.py document.pdf "DRAFT" --output-dir ./results
```

## 🔧 Removal Methods Compared

| Method                 | How it works                                                                    | Best for                                      |
| ---------------------- | ------------------------------------------------------------------------------- | --------------------------------------------- |
| `redactor` (default) | Rewrites the PDF content stream, erasing matched text entirely                  | Text watermarks that must be fully eliminated |
| `pymupdf`            | Draws white rectangles over the watermark text; optionally deletes text objects | Quick visual removal; image watermarks        |

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## 📦 Dependencies

| Package                                               | Purpose                                               |
| ----------------------------------------------------- | ----------------------------------------------------- |
| [PyMuPDF](https://pymupdf.readthedocs.io/)               | PDF parsing, text search, drawing, image manipulation |
| [pdf-redactor](https://github.com/JoshData/pdf-redactor) | Content-stream level text redaction                   |
| [Streamlit](https://streamlit.io/)                       | Web application framework                             |


## License

Licensed under **GNU AGPL v3**.
This project uses [PyMuPDF](https://pymupdf.readthedocs.io/) which is licensed under AGPL v3.

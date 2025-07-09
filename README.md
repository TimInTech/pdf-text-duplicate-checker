# PDF Text & Image Duplicate Checker

This project helps you **detect duplicate PDF files** based on their text content or their visual page content (image hash).

## Features

- **Text-based duplicate detection:**  
  Finds PDFs with identical extractable text (even if filenames differ).
- **Image-based duplicate detection:**  
  Finds visually identical PDFs, even if the text is not extractable (e.g., scans).

## Requirements

- Python 3.8+
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [Pillow](https://python-pillow.org/)
- [ImageHash](https://pypi.org/project/ImageHash/)
- [poppler-utils](https://poppler.freedesktop.org/) (for `pdftoppm`)

Install dependencies with:

```sh
pip install pymupdf pillow imagehash
sudo apt install poppler-utils
```

## Usage

### 1. Text-based duplicate detection

```sh
python src/pdf_text_duplicate_checker.py
```

- Output: List of found duplicates based on extracted text.

### 2. Image-based duplicate detection

```sh
python src/pdf_dupe_imghash.py
```

- Output: List of found visual duplicates (pages are compared as images).

## Folder Structure

- Place all PDFs to be checked in the folder  
  `/home/gummi/Schreibtisch/AllePDF`  
  (or adjust the path in the scripts).

## Notes

- Empty or image-only PDFs are skipped in the text check.
- Temporary image files are deleted automatically.
- The scripts are optimized for Linux.

---

**License:** MIT  
**Author:** TimInTech

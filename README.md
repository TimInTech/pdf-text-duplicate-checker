# PDF Text & Image Duplicate Checker (Advanced)

A powerful tool for detecting duplicate PDF files based on their **text content** (with OCR fallback) and **visual similarity** (image hash).  
Supports batch processing, multithreading, CSV/Markdown export, and Docker deployment.

---

## Features

- **Batch Processing:**  
  Recursively scans a folder and processes all PDF files.
- **Text-based Duplicate Detection:**  
  Extracts and normalizes text from each PDF. If no text is found, uses OCR (Tesseract) to extract text from scanned images.
- **Image-based Duplicate Detection:**  
  (Optional, see `pdf_dupe_imghash.py`) Compares visual similarity of PDF pages using perceptual image hashes.
- **Multithreading:**  
  Processes multiple PDFs in parallel for high performance.
- **CSV & Markdown Export:**  
  Outputs duplicate results as `duplicates.csv` and `duplicates.md`.
- **Docker Support:**  
  Ready-to-use Dockerfile for easy deployment on any system.
- **Customizable:**  
  Configure PDF folder and thread count via environment variables.

---

## Requirements

- Python 3.8+
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [Pillow](https://python-pillow.org/)
- [ImageHash](https://pypi.org/project/ImageHash/)
- [pytesseract](https://pypi.org/project/pytesseract/)
- [poppler-utils](https://poppler.freedesktop.org/) (for `pdftoppm`)
- [tesseract-ocr](https://github.com/tesseract-ocr/tesseract) (for OCR)

Install all dependencies with:

```sh
pip install -r requirements.txt
sudo apt install poppler-utils tesseract-ocr
```

---

## Usage

### Local

1. **Install dependencies** (see above).
2. **Place your PDFs** in a folder (e.g. `/your/pdf/folder`).
3. **Run the script:**
   ```sh
   PDF_DIR=/your/pdf/folder python src/pdf_dupe_advanced.py
   ```
   - You can set the number of threads with `THREADS=8` (default: 4).

### Docker

1. **Build the Docker image:**
   ```sh
   docker build -t pdf-dupe-advanced .
   ```
2. **Run the container:**
   ```sh
   docker run -v /your/pdf/folder:/app/pdfs pdf-dupe-advanced
   ```
   - Results will be written to the project folder inside the container (`/app/duplicates.csv`, `/app/duplicates.md`).

---

## Output

- **duplicates.csv:**  
  A CSV file listing all detected duplicate pairs (original, duplicate).
- **duplicates.md:**  
  A Markdown file with a readable list of all duplicate pairs.

Example CSV:
```
Original,Duplicate
/your/pdf/folder/file1.pdf,/your/pdf/folder/file2.pdf
...
```

Example Markdown:
```
# PDF Duplicates

- **Original:** `/your/pdf/folder/file1.pdf`
  - **Duplicate:** `/your/pdf/folder/file2.pdf`
...
```

---

## How it works

1. **Text Extraction:**  
   For each PDF, the script tries to extract text from every page. If no text is found, it renders the page as an image and uses Tesseract OCR to extract text.
2. **Hashing:**  
   The normalized text is hashed (SHA256). PDFs with the same hash are considered duplicates.
3. **Parallel Processing:**  
   Multiple PDFs are processed in parallel for speed.
4. **Result Export:**  
   All detected duplicates are exported as CSV and Markdown.

---

## Advanced: Visual Duplicate Detection

If you want to find visually identical PDFs (even if the text differs), use `src/pdf_dupe_imghash.py`.  
This script renders each page as an image, computes a perceptual hash, and compares the hashes.

---

## Customization

- **Change PDF folder:**  
  Set the `PDF_DIR` environment variable.
- **Change thread count:**  
  Set the `THREADS` environment variable.
- **Change output file names:**  
  Edit the variables at the top of the script.

---

## Limitations

- OCR quality depends on the quality of scanned PDFs.
- False positives may occur with very similar, but not identical, documents.
- Large collections may require more RAM.

---

## License

MIT

---

## Author

TimInTech

---

## Contributions

Feel free to open issues or submit pull requests for improvements.  
For major changes, please open an issue first to discuss what you would like to change.

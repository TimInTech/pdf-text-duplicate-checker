# PDF Text & Image Duplicate Checker (Advanced)

## Usage

### Local

```sh
pip install -r requirements.txt
sudo apt install poppler-utils tesseract-ocr
PDF_DIR=/your/pdf/folder python src/pdf_dupe_advanced.py
```

### Docker

```sh
docker build -t pdf-dupe-advanced .
docker run -v /your/pdf/folder:/app/pdfs pdf-dupe-advanced
```

- Results: `duplicates.csv` and `duplicates.md` in the project folder.

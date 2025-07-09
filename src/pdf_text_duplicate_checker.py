#!/usr/bin/env python3

import os
import hashlib
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

PDF_DIR = os.environ.get("PDF_DIR", "/app/pdfs")
OUTPUT_CSV = "duplicates.csv"
OUTPUT_MD = "duplicates.md"
THREADS = int(os.environ.get("THREADS", "4"))

def extract_text_with_ocr(page):
    # Try text extraction
    text = page.get_text("text").strip()
    if text:
        return text
    # Fallback: OCR
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    ocr_text = pytesseract.image_to_string(img)
    return ocr_text.strip()

def extract_text_hash(path):
    try:
        with fitz.open(path) as doc:
            texts = []
            for page in doc:
                text = extract_text_with_ocr(page)
                if text:
                    texts.append(text.lower().replace(" ", "").replace("\n", ""))
        if not texts:
            return "EMPTY_OR_IMAGE_ONLY"
        content = "".join(texts)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

def process_pdf(fullpath):
    h = extract_text_hash(fullpath)
    return (fullpath, h)

def main():
    text_hash_map = {}
    duplicates = []

    pdf_files = []
    for root, dirs, files in os.walk(PDF_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_file = {executor.submit(process_pdf, f): f for f in pdf_files}
        for future in as_completed(future_to_file):
            fullpath, h = future.result()
            if h == "EMPTY_OR_IMAGE_ONLY":
                print(f"[SKIP] No extractable text: {os.path.basename(fullpath)}")
                continue
            if h in text_hash_map:
                duplicates.append((text_hash_map[h], fullpath))
            else:
                text_hash_map[h] = fullpath

    # Export CSV
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Original", "Duplicate"])
        for orig, dup in duplicates:
            writer.writerow([orig, dup])

    # Export Markdown
    with open(OUTPUT_MD, "w") as f:
        f.write("# PDF Duplicates\n\n")
        if duplicates:
            for orig, dup in duplicates:
                f.write(f"- **Original:** `{orig}`\n  - **Duplicate:** `{dup}`\n")
        else:
            f.write("No text-based duplicates found.\n")

    # Console output
    if duplicates:
        print("Found duplicates based on text content (see CSV/Markdown):\n")
        for orig, dup in duplicates:
            print(f"Original : {orig}")
            print(f"Duplicate: {dup}")
    else:
        print("No text-based duplicates found.")

if __name__ == "__main__":
    main()
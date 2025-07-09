#!/usr/bin/env python3

import os
import hashlib
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

PDF_DIR = os.environ.get("PDF_DIR", "/home/gummi/Schreibtisch/AllePDF")
OUTPUT_CSV = "duplicates.csv"
OUTPUT_MD = "duplicates.md"
THREADS = int(os.environ.get("THREADS", "4"))
DUPLICATE_DIR = os.path.join(PDF_DIR, "duplikate")

os.makedirs(DUPLICATE_DIR, exist_ok=True)

def extract_text_with_ocr(page):
    text = page.get_text("text").strip()
    if text:
        return text
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return pytesseract.image_to_string(img).strip()

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
        return hashlib.sha256("".join(texts).encode("utf-8")).hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

def process_pdf(fullpath):
    return fullpath, extract_text_hash(fullpath)

def main():
    text_hash_map = {}
    duplicates = []

    pdf_files = []
    for root, dirs, files in os.walk(PDF_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                fullpath = os.path.join(root, file)
                if fullpath.startswith(DUPLICATE_DIR):
                    continue
                pdf_files.append(fullpath)

    print(f"📄 {len(pdf_files)} PDF-Dateien gefunden. Verarbeitung läuft...\n")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(process_pdf, f): f for f in pdf_files}
        for future in tqdm(as_completed(futures), total=len(futures), desc="🔍 Duplikat-Prüfung", unit="Datei"):
            fullpath, h = future.result()
            if h == "EMPTY_OR_IMAGE_ONLY":
                print(f"[SKIP] Kein extrahierbarer Text: {os.path.basename(fullpath)}")
                continue
            if h.startswith("ERROR:"):
                print(f"[FEHLER] {os.path.basename(fullpath)}: {h}")
                continue
            if h in text_hash_map:
                original = text_hash_map[h]
                duplicates.append((original, fullpath))
                target_path = os.path.join(DUPLICATE_DIR, os.path.basename(fullpath))
                shutil.move(fullpath, target_path)
                print(f"[DUPLIKAT] {os.path.basename(fullpath)} -> {target_path}")
            else:
                text_hash_map[h] = fullpath

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Original", "Duplicate"])
        for orig, dup in duplicates:
            writer.writerow([orig, dup])

    with open(OUTPUT_MD, "w") as f:
        f.write("# PDF Duplicates\n\n")
        if duplicates:
            for orig, dup in duplicates:
                f.write(f"- **Original:** `{orig}`\n  - **Duplicate:** `{dup}`\n")
        else:
            f.write("No text-based duplicates found.\n")

    print(f"\n✅ Fertig. {len(duplicates)} Duplikate verschoben.")
    print(f"📄 CSV: {OUTPUT_CSV}")
    print(f"📝 Markdown: {OUTPUT_MD}")

if __name__ == "__main__":
    import shutil
    main()

#!/usr/bin/env python3

import os
import hashlib
import fitz  # PyMuPDF

pdf_dir = "/home/gummi/Schreibtisch/AllePDF"
text_hash_map = {}
duplicates = []

def extract_text_hash(path):
    try:
        with fitz.open(path) as doc:
            texts = []
            for page in doc:
                text = page.get_text("text").strip()
                if text:
                    texts.append(text.lower().replace(" ", "").replace("\n", ""))
        if not texts:
            return "EMPTY_OR_IMAGE_ONLY"
        content = "".join(texts)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

for root, dirs, files in os.walk(pdf_dir):
    for file in files:
        if file.lower().endswith(".pdf"):
            fullpath = os.path.join(root, file)
            h = extract_text_hash(fullpath)
            if h == "EMPTY_OR_IMAGE_ONLY":
                print(f"[SKIP] Kein extrahierbarer Text: {file}")
                continue
            # Seitenanzahl und sortierte Hashes als Schlüssel (für strengen Vergleich)
            # Hier: h ist bereits ein Hash des gesamten Textes, daher bleibt es wie gehabt
            h_key = h
            if h_key in text_hash_map:
                duplicates.append((text_hash_map[h_key], fullpath))
            else:
                text_hash_map[h_key] = fullpath

if duplicates:
    print("Gefundene Duplikate anhand von Textinhalt:\n")
    for orig, dup in duplicates:
        print(f"Original : {orig}")
        print(f"Duplikat : {dup}")
else:
    print("Keine textbasierten Duplikate gefunden.")

# Installiere pymupdf, falls noch nicht geschehen
try:
    import fitz
except ImportError:
    import pip
    pip.main(['install', 'pymupdf'])
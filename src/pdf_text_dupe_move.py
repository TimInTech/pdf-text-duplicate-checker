#!/usr/bin/env python3

import os
import hashlib
import shutil
import fitz  # PyMuPDF

pdf_dir = "/home/gummi/Schreibtisch/AllePDF"
dupe_dir = os.path.join(pdf_dir, "duplikate")
os.makedirs(dupe_dir, exist_ok=True)

text_hash_map = {}
moved_dupes = []

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
        if not file.lower().endswith(".pdf"):
            continue
        fullpath = os.path.join(root, file)
        if fullpath.startswith(dupe_dir):  # ignoriere bereits verschobene
            continue
        h = extract_text_hash(fullpath)
        if h == "EMPTY_OR_IMAGE_ONLY":
            print(f"[SKIP] Kein extrahierbarer Text: {file}")
            continue
        if h.startswith("ERROR:"):
            print(f"[FEHLER] {file}: {h}")
            continue
        if h in text_hash_map:
            print(f"[TEXT-DUPLIKAT] {file} == {os.path.basename(text_hash_map[h])}")
            shutil.move(fullpath, os.path.join(dupe_dir, file))
            moved_dupes.append(file)
        else:
            text_hash_map[h] = fullpath

if moved_dupes:
    print("\nVerschobene Duplikate:")
    for fname in moved_dupes:
        print(f"- {fname}")
else:
    print("Keine textbasierten Duplikate gefunden.")
# Installiere pymupdf, falls noch nicht geschehen
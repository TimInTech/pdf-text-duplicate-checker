#!/usr/bin/env python3

import os
import hashlib
import fitz  # PyMuPDF

PDF_DIR = "/home/gummi/Schreibtisch/AllePDF"
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

for root, dirs, files in os.walk(PDF_DIR):
    for file in files:
        if file.lower().endswith(".pdf"):
            fullpath = os.path.join(root, file)
            h = extract_text_hash(fullpath)
            if h == "EMPTY_OR_IMAGE_ONLY":
                print(f"[SKIP] No extractable text: {file}")
                continue
            h_key = h
            if h_key in text_hash_map:
                duplicates.append((text_hash_map[h_key], fullpath))
            else:
                text_hash_map[h_key] = fullpath

if duplicates:
    print("Found duplicates based on text content:\n")
    for orig, dup in duplicates:
        print(f"Original : {orig}")
        print(f"Duplicate: {dup}")
else:
    print("No text-based duplicates found.")
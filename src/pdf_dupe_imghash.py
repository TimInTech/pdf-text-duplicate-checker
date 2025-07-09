#!/usr/bin/env python3

import os
import shutil
import subprocess
from PIL import Image
import imagehash

PDF_DIR = "/home/gummi/Schreibtisch/AllePDF"
TEMP_IMG_DIR = "/tmp/pdf_dupe_pages"
DUPLICATE_DIR = os.path.join(PDF_DIR, "duplicates")

os.makedirs(TEMP_IMG_DIR, exist_ok=True)
os.makedirs(DUPLICATE_DIR, exist_ok=True)

def pdf_to_hashes(pdf_path, base_name):
    output_base = os.path.join(TEMP_IMG_DIR, base_name)
    subprocess.run(["pdftoppm", "-png", pdf_path, output_base], check=True)
    page_imgs = sorted([
        f for f in os.listdir(TEMP_IMG_DIR)
        if f.startswith(base_name) and f.endswith(".png")
    ])
    page_hashes = []
    for fname in page_imgs:
        with Image.open(os.path.join(TEMP_IMG_DIR, fname)) as im:
            h = imagehash.phash(im)
            page_hashes.append(str(h))
        os.remove(os.path.join(TEMP_IMG_DIR, fname))
    return page_hashes

hash_map = {}
duplicates = []

for fname in sorted(os.listdir(PDF_DIR)):
    if not fname.lower().endswith(".pdf"):
        continue

    path = os.path.join(PDF_DIR, fname)
    base = os.path.splitext(fname)[0]

    try:
        hashes = pdf_to_hashes(path, base)
        h_key = f"{len(hashes)}|" + "|".join(sorted(hashes))  # page count + sorted hashes

        if h_key in hash_map:
            print(f"[DUPLICATE] {fname} == {hash_map[h_key]}")
            duplicates.append(path)
            target = os.path.join(DUPLICATE_DIR, fname)
            if os.path.exists(target):
                print(f"[WARNING] File already exists in duplicates folder: {fname}")
            else:
                shutil.move(path, target)
        else:
            hash_map[h_key] = fname

    except subprocess.CalledProcessError:
        print(f"[ERROR] {fname}: PDF cannot be processed (e.g., password protected)")
    except Exception as e:
        print(f"[ERROR] {fname}: {e}")
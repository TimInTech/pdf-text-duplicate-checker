import os
import subprocess
import imagehash
from PIL import Image
import shutil  # hinzufügen

PDF_DIR = "/home/gummi/Schreibtisch/AllePDF"
TEMP_IMG_DIR = "/tmp/pdf_dupe_pages"
DUPE_DIR = os.path.join(PDF_DIR, "duplikate")  # Zielordner für Duplikate
os.makedirs(TEMP_IMG_DIR, exist_ok=True)
os.makedirs(DUPE_DIR, exist_ok=True)

hash_map = {}
duplicates = []

def pdf_to_hashes(pdf_path, base_name):
    page_hashes = []
    output_base = os.path.join(TEMP_IMG_DIR, base_name)
    # Render alle Seiten als PNG
    subprocess.run(["pdftoppm", "-png", pdf_path, output_base], check=True)
    # Alle gerenderten PNGs für dieses PDF einsammeln
    page_imgs = sorted(
        f for f in os.listdir(TEMP_IMG_DIR)
        if f.startswith(base_name) and f.endswith(".png")
    )
    for fname in page_imgs:
        with Image.open(os.path.join(TEMP_IMG_DIR, fname)) as img:
            h = imagehash.phash(img)
            page_hashes.append(str(h))
        # Optional: temporäre Bilddatei direkt löschen
        os.remove(os.path.join(TEMP_IMG_DIR, fname))
    return page_hashes

for fname in sorted(os.listdir(PDF_DIR)):
    if not fname.lower().endswith(".pdf"):
        continue

    path = os.path.join(PDF_DIR, fname)
    base = os.path.splitext(fname)[0]

    try:
        hashes = pdf_to_hashes(path, base)
        h_key = ",".join(hashes)

        if h_key in hash_map:
            print(f"[DUPLIKAT] {fname} == {hash_map[h_key]}")
            duplicates.append((hash_map[h_key], fname))
            shutil.move(path, os.path.join(DUPE_DIR, fname))  # Duplikat verschieben
        else:
            hash_map[h_key] = fname
    except Exception as e:
        print(f"[FEHLER] {fname}: {e}")
from tqdm import tqdm  # Am Anfang importieren (pip install tqdm)

def main():
    text_hash_map = {}
    duplicates = []

    pdf_files = []
    for root, dirs, files in os.walk(PDF_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    print(f"Found {len(pdf_files)} PDF files. Processing...")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_file = {executor.submit(process_pdf, f): f for f in pdf_files}
        for future in tqdm(as_completed(future_to_file), total=len(pdf_files), desc="Checking PDFs"):
            fullpath, h = future.result()
            if h == "EMPTY_OR_IMAGE_ONLY":
                print(f"[SKIP] No extractable text: {os.path.basename(fullpath)}")
                continue
            if h in text_hash_map:
                duplicates.append((text_hash_map[h], fullpath))
            else:
                text_hash_map[h] = fullpath
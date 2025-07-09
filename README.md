# 🧠 PDF Text & Image Duplicate Checker (Advanced)

**ENGLISH / DEUTSCH**

Ein flexibles Python-Tool zum Finden und Verschieben von doppelten PDF-Dateien – wahlweise durch **Textextraktion (mit OCR-Fallback)** oder **Bildvergleich per Hash**.

A flexible Python tool to detect and move duplicate PDF files – either via **text content (with OCR fallback)** or **image-based perceptual hashing**.

---

## 🔍 Features | Funktionen

- Textvergleich mit OCR (Tesseract), falls kein extrahierbarer Text vorhanden
- Bildvergleich mit `pdftoppm` + perceptual hash (ImageHash)
- Automatisches Verschieben von Duplikaten in einen Unterordner `duplikate`
- Optional: parallele Verarbeitung mit mehreren Threads
- Export als CSV und Markdown
- Docker-Support für plattformunabhängigen Einsatz

---

## ⚙️ Anforderungen | Requirements

```bash
sudo apt install poppler-utils tesseract-ocr python3-venv
pip install -r requirements.txt
```

**Python-Pakete (`requirements.txt`):**

```
pymupdf
pillow
imagehash
pytesseract
```

---

## 📁 Verzeichnisstruktur | Directory Structure

```plaintext
pdf-text-duplicate-checker/
├── src/
│   ├── pdf_dupe_advanced.py          # Hauptskript mit allem (Text + optional OCR)
│   ├── pdf_text_duplicate_checker.py # Textbasierter Scanner mit CSV-/Markdown-Export
│   ├── pdf_text_dupe_move.py         # Textvergleich mit automatischem Verschieben
│   ├── pdf_dupe_imghash.py           # Bildbasierter Vergleich (Verschieben)
├── requirements.txt
├── README.md
```

---

## 🚀 Verwendung | Usage

### 🧪 Variante 1: Textbasierter Check mit Export

Scannt alle PDFs rekursiv und exportiert Ergebnisse in `duplicates.csv` + `duplicates.md`.

```bash
PDF_DIR=/pfad/zur/pdf-sammlung THREADS=8 python src/pdf_text_duplicate_checker.py
```

### 🚚 Variante 2: Textbasierter Vergleich + Verschieben

Alle erkannten Duplikate werden direkt in `duplikate/` verschoben.

```bash
python src/pdf_text_dupe_move.py
```

### 🖼️ Variante 3: Bildvergleich (Seiteninhalt)

Render-basierter Abgleich auf Basis der visuellen Ähnlichkeit von PDF-Seiten.

```bash
python src/pdf_dupe_imghash.py
```

### 🧠 Variante 4: Alles in einem – mit Multithreading

OCR bei Bedarf, paralleles Scanning, automatisches Erkennen, Export in CSV/MD.

```bash
PDF_DIR=/pfad/zur/pdf-sammlung THREADS=4 python src/pdf_dupe_advanced.py
```

---

## 🐳 Docker

**Image bauen:**

```bash
docker build -t pdf-dupe-checker .
```

**Container ausführen:**

```bash
docker run -v /deine/pdfs:/app/pdfs pdf-dupe-checker
```

Ergebnisse liegen dann in `/app/duplicates.csv` und `.md`.

---

## 📤 Ergebnisformate

### CSV (`duplicates.csv`)
```csv
Original,Duplicate
file1.pdf,file1_copy.pdf
```

### Markdown (`duplicates.md`)
```markdown
# PDF Duplicates

- **Original:** `file1.pdf`
  - **Duplicate:** `file1_copy.pdf`
```

---

## 🔐 Sicherheit & Verhalten

- ❌ **Keine Datei wird gelöscht**
- ✅ Duplikate werden **nur verschoben** (nicht überschrieben)
- 🔄 Wiederholbares Scannen möglich

---

## 🧪 Bekannte Einschränkungen

- OCR kann bei schlechter Scanqualität unzuverlässig sein
- Visuelle Duplikaterkennung ist rechenintensiver (langsamer)
- Sehr große Ordner benötigen mehr RAM

---

## 👨‍💻 Autor / Author

**TimInTech**  
→ GitHub: [@TimInTech](https://github.com/TimInTech)

---

## 🤝 Beiträge willkommen

Pull Requests, Bug Reports und Verbesserungsvorschläge sind jederzeit willkommen.

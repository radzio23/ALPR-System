# ALPR – Instrukcja uruchomienia

Projekt realizuje automatyczne rozpoznawanie tablic rejestracyjnych (ALPR) z użyciem Python + OpenCV + Tesseract.

## 1. Wymagania

- Python 3.8+
- Zainstalowany Tesseract OCR  
  (Windows: https://github.com/tesseract-ocr/tesseract)

## 2. Instalacja zależności

W katalogu projektu uruchomić:

```bash
pip install opencv-python pytesseract imutils numpy
```
## 3. Konfiguracja Tesseract
W pliku ocr.py ustawić ścieżkę do Tesseract:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

## 4. Uruchomienie programu
python src/main.py

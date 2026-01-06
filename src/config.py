import os
import pytesseract

# Ścieżka do pliku wykonywalnego Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'P:\coding\tesseract\tesseract.exe'
# Folder ze zdjęciami wejściowymi
INPUT_FOLDER = '../data'
# Ścieżka do pliku kaskady Haar Cascade
CASCADE_PATH = 'haarcascade_plate.xml'

# Sprawdzanie zasobów
if not os.path.exists(CASCADE_PATH):
    print(f"BŁĄD: Nie znaleziono pliku {CASCADE_PATH}")
    exit()

if not os.path.exists(INPUT_FOLDER):
    print(f"BŁĄD: Nie znaleziono folderu {INPUT_FOLDER}")
    os.makedirs(INPUT_FOLDER)
    print(f"Utworzono pusty folder {INPUT_FOLDER}.")
    exit()
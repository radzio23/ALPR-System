import cv2
import imutils
import numpy as np
import pytesseract
import os
import re

from preprocessing import preprocess_for_ocr
from utils import fix_polish_plate
from config import INPUT_FOLDER, CASCADE_PATH

# Inicjalizacja klasyfikatora Haar Cascade
plate_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Główna funkcja przetwarzająca pojedynczy obraz
def process_image(filename):
    print(f"\n--- Analiza: {filename} ---")
    path = os.path.join(INPUT_FOLDER, filename)
    img = cv2.imread(path)
    if img is None: return

    # Zmiana rozmiaru obrazu
    img = imutils.resize(img, width=800)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Szukanie tablic - detekcja kaskadą Haar
    plates = plate_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))

    if len(plates) == 0:
        print("Nie wykryto tablicy.")
        cv2.imshow("Wynik", img)
        cv2.waitKey(0)
        return

    best_text = ""
    best_conf = 0
    best_roi = None

    # Iteracja przez wszystkie znalezione tablice
    for (x, y, w, h) in plates:
        roi = gray[y:y+h, x:x+w]
    
        processed_roi = preprocess_for_ocr(roi)
        
        # Konifiguracja OCR 
        # --psm 8: obraz jako pojedyncze słowo
        # whitelist - szukanie tylko liter i cyfr
        config = r'--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        try:
            raw_text = pytesseract.image_to_string(processed_roi, config=config)
            print(f"OCR surowy tekst: {raw_text.strip()}")
            clean_t = fix_polish_plate(raw_text)

            # System oceny wyniku
            score = 0
            if len(clean_t) >= 7 and len(clean_t) <= 8: score += 10
            if len(clean_t) > 0 and clean_t[0].isalpha(): score += 5

            if score > best_conf:
                best_conf = score
                best_text = clean_t
                best_coords = (x, y, w, h)
                best_roi = processed_roi

        except Exception as e:
            print(f"Błąd Tesseracta: {e}")

    # Wyświetlanie wyników
    if best_conf > 0:
        x, y, w, h = best_coords
        print(f"SUKCES: {best_text}")
        # Rysowanie ramki i tekstu na obrazie wyjściowym
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, best_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.imshow("DEBUG: Tesseract Input", best_roi)
    else:
        print("Wykryto tablicę, ale nie udało się odczytać tekstu.")

    cv2.imshow("Wynik", img)
    
    # Obsługa klawiatury
    key = cv2.waitKey(0) & 0xFF
    if key == 27:  # ESC
        print("Zamykanie programu...")
        cv2.destroyAllWindows()
        exit() 

def main():
    # Pobieranie listy plików i sortowanie
    files = os.listdir(INPUT_FOLDER)
    # files.sort()
    
    for file in files:
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            process_image(file)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
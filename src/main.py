import os
import cv2
import imutils

from detector import load_cascade, detect_with_haar, find_plate_contours
from preprocessing import preprocess_roi
from ocr import ocr_read
from utils import expand_bbox

INPUT_FOLDER = '../data/test_samples'
CASCADE_PATH = 'haarcascade_plate.xml'

def process_image(filename, cascade):
    print(f"\n--- Analiza: {filename} ---")
    path = os.path.join(INPUT_FOLDER, filename)
    img = cv2.imread(path)
    if img is None:
        return

    img = imutils.resize(img, width=800)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_h, img_w = gray.shape

    candidates = []

    candidates += detect_with_haar(gray, cascade)

    cont = find_plate_contours(gray)
    if cont:
        candidates.append(cont)

    if not candidates:
        print("Nie wykryto tablicy.")
        return

    best_text = ""
    best_score = 0
    best_coords = None
    best_roi = None

    for method, (x, y, w, h) in candidates:
        nx, ny, nw, nh = expand_bbox(x, y, w, h, img_w, img_h)
        roi = gray[ny:ny+nh, nx:nx+nw]

        processed = preprocess_roi(roi)
        text, score = ocr_read(processed)

        if score > best_score:
            best_score = score
            best_text = text
            best_coords = (x, y, w, h)
            best_roi = processed

    if best_score > 0:
        x, y, w, h = best_coords
        print(f"ODCZYT: {best_text}")
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, best_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Tesseract view", best_roi)
    else:
        print("Tablica wykryta, ale nie odczytano tekstu.")

    cv2.imshow("Wynik", img)
    cv2.waitKey(0)

def main():
    cascade = load_cascade(CASCADE_PATH)
    files = os.listdir(INPUT_FOLDER)

    for file in files:
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            process_image(file, cascade)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

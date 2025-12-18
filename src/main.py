import cv2
import imutils
import numpy as np
import pytesseract
import os
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # o tu ta sciezke trzeba ustawic swoja jesli ma sie inna

INPUT_FOLDER = '../data/test_samples'
OUTPUT_FOLDER = '../results'
CASCADE_PATH = 'haarcascade_plate.xml'

if not os.path.exists(CASCADE_PATH):
    print(f"BŁĄD: Nie znaleziono pliku {CASCADE_PATH} (powinien być w katalogu src)")
    exit()

plate_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# poprawki dla polskich tablic rejestracyjnych
def fix_polish_plate(text):
    text = list(text)

    dict_int_to_char = {'0': 'O', '1': 'I', '2': 'Z', '8': 'B', '5': 'S', '4': 'A', '6': 'G'}

    dict_char_to_int = {'O': '0', 'I': '1', 'Z': '2', 'B': '8', 'S': '5', 'A': '4', 'G': '6'}

    for i in range(min(len(text), 2)):
        if text[i] in dict_int_to_char:
            text[i] = dict_int_to_char[text[i]]

    if len(text) >= 7:
        for i in range(len(text)-4, len(text)):
            if text[i] in dict_char_to_int:
                text[i] = dict_char_to_int[text[i]]

    return "".join(text)

def clean_text(text):
    return re.sub(r'[^A-Z0-9]', '', text.upper())


def preprocess_roi(roi):
    roi = cv2.resize(roi, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    
    if len(roi.shape) == 3:
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(roi, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    if np.sum(thresh == 255) < thresh.size * 0.5:
        thresh = cv2.bitwise_not(thresh)

    h, w = thresh.shape
    
    border_h = int(h * 0.05) + 5
    border_w_left = int(w * 0.08)
    border_w_right = int(w * 0.02)
    
    thresh = thresh[border_h:h-border_h, border_w_left:w-border_w_right]
    
    thresh = cv2.copyMakeBorder(thresh, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    
    return thresh


def find_plate_contours(gray):
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blurred, 30, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:15]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            aspect = w / float(h)
            if 2.5 < aspect < 6.0 and h > 20:
                return (x, y, w, h)
                
    return None


def process_image(filename):
    print(f"\n--- Analiza: {filename} ---")
    path = os.path.join(INPUT_FOLDER, filename)
    img = cv2.imread(path)
    if img is None: return

    img = imutils.resize(img, width=800)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_h, img_w = gray.shape

    candidates = []

    plates_haar = plate_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))
    for p in plates_haar:
        candidates.append(("Haar", p))

    cont_rect = find_plate_contours(gray)
    if cont_rect:
        candidates.append(("Contours", cont_rect))

    if not candidates:
        print("Nie wykryto kształtu tablicy.")
        return

    best_result = ""
    best_score = 0
    best_coords = None
    best_roi_debug = None

    for method, (x, y, w, h) in candidates:
        
        
        pad_w = int(w * 0.1)
        pad_h = int(h * 0.15)

        nx = max(0, x - pad_w)
        ny = max(0, y - pad_h)
        nw = min(img_w, x + w + pad_w*2) - nx
        nh = min(img_h, y + h + pad_h*2) - ny

        roi = gray[ny:ny+nh, nx:nx+nw]
        
        processed_roi = preprocess_roi(roi)

        for psm in [7, 6]:
            config = f'--psm {psm} -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            text = pytesseract.image_to_string(processed_roi, config=config)
            
            clean = clean_text(text)
            fixed = fix_polish_plate(clean)

            score = 0
            if len(fixed) >= 4: score += 10
            if len(fixed) <= 9: score += 5
            if len(fixed) > 2 and fixed[:2].isalpha(): score += 20 
            
            if score > best_score:
                best_score = score
                best_result = fixed
                best_coords = (x, y, w, h)
                best_roi_debug = processed_roi

    if best_score > 0:
        x, y, w, h = best_coords
        print(f"ODCZYT: {best_result}")
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, best_result, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if best_roi_debug is not None:
            cv2.imshow("Tesseract view", best_roi_debug)
    else:
        print("Wykryto tablice, ale nie da sie odczytac")
        for _, (x,y,w,h) in candidates:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 1)

    cv2.imshow("Wynik", img)
    cv2.waitKey(0)

def main():
    files = os.listdir(INPUT_FOLDER)
    for file in files:
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            process_image(file)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
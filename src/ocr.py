import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def clean_text(text):
    return re.sub(r'[^A-Z0-9]', '', text.upper())

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

def ocr_read(processed_roi):
    best = ""
    best_score = 0

    for psm in [7, 6]:
        config = f'--psm {psm} -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        raw = pytesseract.image_to_string(processed_roi, config=config)

        clean = clean_text(raw)
        fixed = fix_polish_plate(clean)

        score = 0
        if len(fixed) >= 4: score += 10
        if len(fixed) <= 9: score += 5
        if len(fixed) > 2 and fixed[:2].isalpha(): score += 20

        if score > best_score:
            best_score = score
            best = fixed

    return best, best_score

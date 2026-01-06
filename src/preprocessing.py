import cv2
import numpy as np

# Przygotowanie wyciętego fragmentu tablicy (ROI) pod OCR.
def preprocess_for_ocr(roi):
    h, w = roi.shape
    # Przycinanie
    crop_h = int(h * 0.1) 
    crop_w = int(w * 0.05)
    roi = roi[crop_h:h-crop_h, crop_w*2:w-crop_w]
    
    # Skalowanie
    target_height = 200
    scale = target_height / roi.shape[0]
    roi = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    # Rozmycie Gaussa - redukcja szumów
    roi = cv2.GaussianBlur(roi, (5, 5), 0)

    # Progowanie Otsu - zamiana na obraz binarny
    _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Czyszczenie - operacja morfologiczna 'open'
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # Kontrola kolorów - czarny tekst na białym tle
    total_pixels = thresh.size
    white_pixels = cv2.countNonZero(thresh)
    if white_pixels < (total_pixels * 0.5):
        thresh = cv2.bitwise_not(thresh)
        
    # Pogrubienie - erozja
    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    
    return thresh
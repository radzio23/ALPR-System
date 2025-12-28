import cv2
import imutils

def load_cascade(path):
    return cv2.CascadeClassifier(path)

def detect_with_haar(gray, cascade):
    plates = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(30, 30)
    )
    return [("Haar", p) for p in plates]

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
                return ("Contours", (x, y, w, h))

    return None

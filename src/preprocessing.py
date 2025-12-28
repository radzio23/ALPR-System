import cv2
import numpy as np

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
    thresh = cv2.copyMakeBorder(thresh, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255])

    return thresh

# 🚗 ALPR – Automatic License Plate Recognition
This project provides an automated solution for detecting and reading vehicle license plates using Python, OpenCV, and Tesseract OCR.

## 🛠️ Setup instructions
### 1. Requirements
* Python 3.8+
* Tesseract OCR: (https://github.com/tesseract-ocr/tesseract/wiki/Home/184342af4939bfdac749fee3337b84145dc00bdb)

### 2. Installation
Clone the repository and install the required Python dependencies using pip:
```
pip install -r requirements.txt
```
### 3. Configuration
   
Since Tesseract is an external binary, you need to specify its location in your code. Open ocr.py and set the tesseract_cmd path:
```
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
### 4. Usage
To run the recognition script, execute the main entry point from your terminal:
```
python src/main.py
```
### 5. How It Works
*Preprocessing: The image is converted to grayscale and blurred to reduce noise.
*Edge Detection: We use Canny edge detection to find the outlines of objects.
*Contour Filtering: The algorithm searches for rectangular shapes that match the proportions of a license plate.
*OCR: Tesseract extracts the alphanumeric characters from the identified region.




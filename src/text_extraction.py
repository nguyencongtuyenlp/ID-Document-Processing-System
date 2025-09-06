import pytesseract
import os
import cv2
from .data_normalization import count_invalid_characters

# Tự động set đường dẫn Tesseract cho Windows
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Set TESSDATA_PREFIX
    os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

def extract_text(image):
    text = pytesseract.image_to_string(image, lang='Vietnamese+eng')
    return [line.strip() for line in text.split('\n') if line.strip()]

def extract_text_from_roi(image):
    # Chuyển ảnh màu sang grayscale cho OCR
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image
    
    text = pytesseract.image_to_string(gray_image, lang='Vietnamese')
    invalid_count = count_invalid_characters(text)
    total_chars = len(text.replace(' ', ''))
    if total_chars > 0 and (invalid_count / total_chars) > 0.5:
        return ""
    return text.strip() if text.strip() else ""

def extract_text_from_roi_mrz(image):
    text = pytesseract.image_to_string(image, lang='ocrb+eng')
    return text.strip() if text.strip() else ""
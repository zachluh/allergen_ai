import pytesseract
from PIL import Image
import os
import cv2
import easyocr


if os.getenv("FLASK_ENV") == "local":
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH")




def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    scale_factor = 2
    resized = cv2.resize(binary, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    return resized


def read(image_path):
    processed_image = Image.fromarray(preprocess_image(image_path))
    text = pytesseract.image_to_string(processed_image, lang='eng')
    print(text)

    os.remove(image_path)

    return text







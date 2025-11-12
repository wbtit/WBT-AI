import io
import cv2
import os
from google.cloud import vision

def preprocess_for_ocr(file_path: str) -> str:
    """
    Preprocess image to improve OCR accuracy on CAD-style drawings.
    - Converts to grayscale
    - Increases contrast
    - Removes line noise
    """
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return file_path  # Not an image (maybe PDF)

    # Increase contrast and invert colors for better OCR
    img = cv2.bitwise_not(img)
    img = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    processed_path = file_path.replace(".png", "_pre.png").replace(".jpg", "_pre.jpg")
    cv2.imwrite(processed_path, img)
    return processed_path

def extract_text(file_path: str) -> str:
    """
    Extract text from engineering drawings using Vision Document OCR.
    Uses preprocessing + document_text_detection.
    """
    client = vision.ImageAnnotatorClient()

    processed_path = preprocess_for_ocr(file_path)
    with io.open(processed_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(f"Vision API error: {response.error.message}")

    full_text = response.full_text_annotation.text
    print("\n===== OCR Extracted Text Preview =====\n", full_text[:800], "\n====================================\n")

    return full_text or ""

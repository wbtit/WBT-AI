import pytesseract
import cv2
import fitz
import os

def extract_text_from_pdf(file_path:str)->str:
    """Extract raw text from PDF using PyMuPDF"""
    doc = fitz.open(file_path)
    text=""
    for page in doc:
        text+=page.get_text()
    return text

def extract_text_from_image(file_path:str)->str:
    """Extract text from image using pytesseract"""
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def ai_estimate(file_path:str):
    """
    MAIN AI LOGIC:
        1.Dtetct file type
        2.extract raw text
        3.process into structured estimations          
    """
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext in ['.pdf']:
        raw_text = extract_text_from_pdf(file_path)
    elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
        raw_text = extract_text_from_image(file_path)
    else:
        raw_text = "Unsupported file type"
        
    # TEMP MOCK: Replace this later with real extraction logic
    return {
        "raw_text": raw_text[:500],  # first 500 chars
        "estimations": [
            {"category": "Beam", "width": 300, "height": 500, "material": "Concrete"},
            {"category": "Column", "width": 400, "height": 400, "material": "Steel"},
        ]
    }
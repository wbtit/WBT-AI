import io
import os
from google.cloud import vision

# It's more efficient to initialize the client once and reuse it.
client = vision.ImageAnnotatorClient()

def extract_text_gcp(file_path:str)->str:
    """Extract text from image/PDF using Google Cloud Vision API"""
    
    with io.open(file_path,"rb") as image_file:
        content = image_file.read()
        
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    
    if response.error.message:
        raise Exception(f'Google Vision API Error: {response.error.message}')
    
    return response.full_text_annotation.text
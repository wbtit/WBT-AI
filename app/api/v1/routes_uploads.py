from fastapi import APIRouter, UploadFile, File
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import shutil

load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH")

router = APIRouter()

@router.post("/")
async def upload_drawing(file: UploadFile = File(...)):
    os.makedirs(STORAGE_PATH, exist_ok=True)
    # Sanitize the filename to prevent path traversal attacks
    safe_filename = secure_filename(file.filename)
    file_path = os.path.join(STORAGE_PATH, safe_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": safe_filename, "detail": "File uploaded successfully"}
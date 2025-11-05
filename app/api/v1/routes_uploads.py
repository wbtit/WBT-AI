from fastapi import APIRouter, UploadFile, File,Depends,HTTPException
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from sqlmodel import Session
from db.session import get_session
from core.deps import get_current_user
from models.user_model import User
from services.file_service import FileService
from models.drawing_model import Drawing



load_dotenv()
STORAGE_PATH = os.getenv("STORAGE_PATH")

router = APIRouter()

@router.post("/")
async def upload_drawing(
    file:UploadFile=File(...),
    session:Session= Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if not file.content_type:
        raise HTTPException(status_code=400,detail="Invalid file type")
    file_path  = await FileService.save_file(file)
    
    drawing = Drawing(
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        uploader_id=current_user.id
    )
    
    session.add(drawing)
    session.commit()
    session.refresh(drawing)
    return drawing

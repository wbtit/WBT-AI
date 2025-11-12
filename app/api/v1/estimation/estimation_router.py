from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, status
from sqlmodel import Session, select
from models.estimation_model import Estimation, Project
from models.drawing_model import Drawing
from models.user_model import User
from schemas.estimation_schema import EstimationRead
from services.file_service import FileService
from services.estimation_service import run_ai_estimation
from db.session import get_session
from core.deps import get_current_user
from typing import List
import logging

logging.basicConfig(filename="ai_debug.log", level=logging.INFO)

router = APIRouter()

@router.post("/upload")
async def upload_drawing(
    project_id: int = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_path = await FileService.save_file(file)
    drawing = Drawing(
        filename=file.filename,
        file_path=file_path,
        project_id=project_id,
        uploader_id=current_user.id,
        file_type=file.content_type
    )
    session.add(drawing)
    session.commit()
    session.refresh(drawing)
    
    return drawing


@router.get("/list", response_model=List[EstimationRead])
async def list_estimations(
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    estimations = session.exec(
        select(Estimation).join(Drawing).where(Drawing.project_id == project_id)
    ).all()
    
    return estimations


@router.post("/ai-mvp/{drawing_id}", response_model=dict)
def estimate_drawing_ai(
    drawing_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Run AI estimation on a drawing and save results to database."""
    
    # Verify drawing exists
    drawing = session.get(Drawing, drawing_id)
    if not drawing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drawing not found")
    
    # Run AI estimation
    estimations = run_ai_estimation(drawing.file_path, drawing_id, session)
    
    # Refresh to get IDs and other fields
    session.refresh(drawing)
    
    # Convert estimations to dicts for serialization
    results = [
        {
            "id": est.id,
            "drawing_id": est.drawing_id,
            "category": est.category,
            "width": est.width,
            "height": est.height,
            "material": est.material,
            "cost": est.cost,
            "created_at": est.created_at.isoformat(),
            "updated_at": est.updated_at.isoformat()
        }
        for est in estimations
    ]
    
    return {
        "message": "AI estimation complete",
        "count": len(estimations),
        "results": results
    }
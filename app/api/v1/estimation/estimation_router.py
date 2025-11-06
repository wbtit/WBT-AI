from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from sqlmodel import Session, select
from core.file_storage import save_file
from models.estimation_model import Drawing, Estimation, Project
from services.estimation_service import generate_estimation
from db.session import get_session

router = APIRouter(prefix="/estimation", tags=["Estimation"])

@router.post("/upload")
async def upload_drawing(
    project_id:int= Form(...),
    file:UploadFile=Form(...),
    session:Session = Depends(get_session)
):
    project= session.get(Project,project_id)
    if not project:
        raise HTTPException(status_code=404,detail="Project not found")
    
    file_path = save_file(file)
    drawing = Drawing(filename=file.filename,file_path=file_path,project_id=project_id)
    session.add(drawing)
    session.commit()
    session.refresh(drawing)
    return {"message":"File uploaded successfully","drawing":drawing}

@router.post("estimate/{drawing_id}")
def estimate_drawing(drawing_id:int,session:Session=Depends(get_session)):
    drawing = session.get(Drawing,drawing_id)
    if not drawing:
        raise HTTPException(status_code=404,detail="Drawing not found")
    estimates=generate_estimation(drawing.file_path)
    for e in estimates:
        est = Estimation(**e,drawing_id=drawing_id)
        session.add(est)
    session.commit()
    return {"message":"Estimation completed","estimations":estimates}
    
@router.get("/list")
def list_estimations(project_id:int,session:Session=Depends(get_session)):
    statement =(
        select(Estimation)
        .join(Drawing)
        .where(Drawing.project_id == project_id)
    )
    results = session.exec(statement).all()
    return {"estimations":results}
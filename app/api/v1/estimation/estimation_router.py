from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from sqlmodel import Session, select
# You would need to import your new schemas here
from models.estimation_model import  Estimation, Project
from models.drawing_model import Drawing
from models.user_model import User
from services.file_service import FileService
from services.estimation_service import ai_estimate
from db.session import get_session
from core.deps import get_current_user
from services.vision_service import extract_text_gcp
from services.vertex_estimation_service import extract_structured_estimate

router = APIRouter()

@router.post("/upload")
async def upload_drawing(
    project_id:int= Form(...),
    file:UploadFile=File(...),
    session:Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    project= session.get(Project,project_id)
    if not project:
        raise HTTPException(status_code=404,detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this project")
    
    file_path = await FileService.save_file(file)
    drawing = Drawing(filename=file.filename,file_path=file_path,project_id=project_id,uploader_id=current_user.id,file_type=file.content_type)
    session.add(drawing)
    session.commit()
    session.refresh(drawing)
    return {"message":"File uploaded successfully","drawing":drawing}

# @router.post("/estimate/{drawing_id}")
# async def estimate_drawing(
#     drawing_id:int,
#     session:Session=Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     drawing = session.get(Drawing,drawing_id)
#     if not drawing:
#         raise HTTPException(status_code=404,detail="Drawing not found")
    
#     # Authorization check
#     project = session.get(Project, drawing.project_id)
#     if not project or project.owner_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not authorized to access this drawing")

#     estimates=generate_estimation(drawing.file_path)
#     for e in estimates:
#         est = Estimation(**e,drawing_id=drawing_id)
#         session.add(est)
#     session.commit()
#     return {"message":"Estimation completed","estimations":estimates}

@router.get("/list")
async def list_estimations(
    project_id:int,
    session:Session=Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Authorization check
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view estimations for this project")

    statement =(
        select(Estimation)
        .join(Drawing)
        .where(Drawing.project_id == project_id)
    )
    results = session.exec(statement).all()
    return {"estimations":results}

# @router.post("/ai-estimate/{drawing_id}")
# def ai_estimate_drawing(
#     drawing_id:int,
#     session:Session=Depends(get_session),
#     current_user: User = Depends(get_current_user)
# ):
#     drawing = session.get(Drawing,drawing_id)
#     if not drawing:
#         raise HTTPException(status_code=404,detail="Drawing not found")
    
#     result = ai_estimate(drawing.file_path)
    
#     for item in result["estimations"]:
#         est = Estimation(
#             drawing_id=drawing.id,
#             category=item["category"],
#             width=item["width"],
#             height=item["height"],
#             material=item["material"],
#             cost=None
#         )
#         session.add(est)
#     session.commit()
#     return {"message":"AI Estimation completed","raw_text":result["raw_text"],"estimations":result["estimations"]}
        
        

@router.post("/ai-full/{drawing_id}")
async def ai_full_estimate(drawing_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    drawing = session.get(Drawing, drawing_id)
    print("Drawing ID:*********************************", drawing_id)
    print("Drawing:", drawing)
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")

    # Step 1 — Extract text from PDF/image
    raw_text = extract_text_gcp(drawing.file_path)

    # Step 2 — Ask Gemini/Vertex AI to structure it
    estimations = extract_structured_estimate(raw_text)

    # Step 3 — Save to DB
    for e in estimations:
        est = Estimation(
            drawing_id=drawing.id,
            category=e.get("type", "Unknown"),
            width=e.get("width", 0),
            height=e.get("height", 0),
            material=e.get("material", "Unknown"),
            cost=None
        )
        session.add(est)

    session.commit()
    return {"message": "AI Estimation Completed!", "data": estimations}
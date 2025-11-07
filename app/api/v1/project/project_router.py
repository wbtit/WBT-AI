from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from core.file_storage import save_file
from schemas.project_schema import Projectcreate, Projectread, Projectlist, Projectupdate,Projectdelete
from models.estimation_model import Project
from models.user_model import User
from db.session import get_session
from core.deps import get_current_user

router = APIRouter()

@router.post("/create")
async def create_project(
    project: Projectcreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_project = Project(**project.dict(), owner_id=current_user.id)
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return {"message": "Project created successfully", "project": new_project}

@router.get("/list", response_model=List[Projectlist])
async def list_projects(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    projects = session.exec(select(Project).where(Project.owner_id == current_user.id)).all()
    return projects



@router.get("/{project_id}", response_model=Projectread)
async def get_project(
    project_id:int,
    session:Session=Depends(get_session),
    current_user : User= Depends(get_current_user)
):
    # A more direct way to fetch a single item by primary key and check ownership
    project = session.get(Project, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this project")
    return project
        
@router.put("/{project_id}")
async def update_project(
    project_id:int,
    project_update:Projectupdate,
    session:Session=Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    project = session.get(Project,project_id)
    if not project:
        raise HTTPException(status_code=404,detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this project")

    project_data= project_update.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(project, key, value)

    session.add(project)
    session.commit()
    session.refresh(project)
    return {"message":"Project updated successfully","project":project}

@router.delete("/{project_id}")
async def delete_project(
    project_id:int,
    session:Session=Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    project = session.get(Project,project_id)
    if not project:
        raise HTTPException(status_code=404,detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")
    
    session.delete(project)
    session.commit()
    return {"message":"Project deleted successfully"}
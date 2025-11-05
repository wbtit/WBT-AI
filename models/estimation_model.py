from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,List
from datetime import datetime, timezone
from models.drawing_model import Drawing
from models.user_model import User

class Project(SQLModel,tabel=True):
    id:int=Field(default=None,primary_key=True)
    name:str
    description:Optional[str]=None
    created_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
    owner_id:int =Field(foreign_key="user.id")
    
    #Relationships
    drawings:List["Drawing"] = Relationship(back_populates="project")
    
    class Drawing(SQLModel,table=True):
        id:int= Field(default=None,primary_key=True)
        filename:str
        file_path:str
        file_type:Optional[str]=None
        uploaded_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
        created_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
        updated_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
        uploader_id: Optional[int] = Field(default=None, foreign_key="user.id")
        project_id: Optional[int] = Field(default=None, foreign_key="project.id")

        #Relationships
        uploader:Optional["User"]= Relationship(back_populates="drawings")
        project:Optional["Project"]= Relationship(back_populates="drawings")
        estimations:List["Estimation"]= Relationship(back_populates="drawing")
        
        
    class Estimation(SQLModel,table=True):
        id:int= Field(default=None,primary_key=True)
        drawing_id:int= Field(foreign_key="drawing.id")
        category:str
        width:float
        height:float
        material:str
        cost:Optional[float]=None
        created_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))
        updated_at:datetime=Field(default_factory=lambda: datetime.now(timezone.utc))

        #Relationships
        drawing:Optional["Drawing"]= Relationship(back_populates="estimations")
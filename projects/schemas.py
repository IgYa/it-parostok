from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class ProjectAdd(BaseModel):
    """ Scheme of validation of visible fields of the ProjectOrm """
    user_id: int

    title: str
    text: Optional[str] = ""
    views: Optional[int] = 0
    likes: Optional[int] = 0
    tags: Optional[List[str]] = []

    contenttype: str
    orientation: str
    size: str
    colorscheme: str
    popularity: str

    cat_id: int
    created_at: datetime
    photos: Optional[List[str]] = []



class Project(ProjectAdd):
    """ Scheme of validation of invisible fields of the ProjectOrm """
    id: int

    updated_at: datetime
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class Categoria(BaseModel):
    """ Scheme of validation of fields of the CategoriaOrm """
    id: int
    name: str
    description: Optional[str] = ""
    is_active: bool
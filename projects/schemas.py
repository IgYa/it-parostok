from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class ProjectAdd(BaseModel):
    """ Scheme of validation of visible fields of the ProjectOrm """
    cat_id: int
    title: str
    text: Optional[str] = ""
    photos: Optional[List[str]] = []
    is_active: bool


class Project(ProjectAdd):
    """ Scheme of validation of invisible fields of the ProjectOrm """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Categoria(BaseModel):
    """ Scheme of validation of fields of the CategoriaOrm """
    id: int
    name: str
    description: Optional[str] = ""
    is_active: bool
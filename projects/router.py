from fastapi import APIRouter, Depends, UploadFile, Form, File
from projects.schemas import ProjectAdd, Project
from projects.repo import ProjectsRepo
from users.schemas import User
from users.dependcies import get_current_user, get_current_superuser
from typing import Optional


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/add")
async def create_project(
    # user_id: int = Form(...),  # тестовий ввод без авторізації
    title: str = Form(...),
    text: str = Form(...),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    user: User = Depends(get_current_user)
):
    """ Add a new Project """

    photos = []

    # Check if there is an image file (optional field)
    if image:
        # Uploading image file and getting the new filenames
        photos = [await ProjectsRepo.add_image(image)]

    data = ProjectAdd(title=title, text=text, photos=photos, is_active=is_active)
    await ProjectsRepo.set_one(
                            user_id=user.id,  # user_id,  #
                            title=data.title,
                            text=data.text,
                            photos=data.photos,
                            is_active=data.is_active)
    return {"result": "Project added successfully"}


@router.get("/user")
async def get_user_projects(current_user: User = Depends(get_current_user)) -> list[Project]:
    """ Get all Projects for current user """
    return await ProjectsRepo.get_all(user_id=current_user.id)


@router.get("/all")
async def get_all_projects(current_user: User = Depends(get_current_superuser)) -> list[Project]:
    """ Get all Projects, only superuser"""
    if current_user:
        return await ProjectsRepo.get_all()


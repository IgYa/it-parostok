from fastapi import APIRouter, Depends, UploadFile, Form, File
from fastapi.responses import FileResponse

from projects.schemas import ProjectAdd, Project
from projects.repo import ProjectsRepo
from users.schemas import User
from users.dependcies import get_current_user, get_current_superuser
from typing import Optional
from config import PATH_IMAGES

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/add")
async def create_project(
    # user_id: int = Form(...),  # тестовий ввод без авторізації
    cat_id: int = Form(...),
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

    data = ProjectAdd(cat_id=cat_id, title=title, text=text, photos=photos, is_active=is_active)
    await ProjectsRepo.set_one(
                            user_id=user.id,  # user_id
                            cat_id=data.cat_id,
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
async def get_all_projects() -> list[Project]:  #
    """ Get all Projects"""
    # current_user: User = Depends(get_current_superuser)
    # if current_user:
    return await ProjectsRepo.get_all()


@router.get("/active")
async def get_active_projects() -> list[dict]:  #
    """ Get all Projects"""
    # current_user: User = Depends(get_current_superuser)
    # if current_user:
    return await ProjectsRepo.get_active_projects()


# @router.get("/image/{file_name}", response_class=FileResponse)
# async def show_file(file_name: str) -> str:
#     """ Show image from PATH_IMAGES"""
#     path = f"{PATH_IMAGES}{file_name}"
#     return path

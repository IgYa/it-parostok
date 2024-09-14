from typing import Optional
from fastapi import APIRouter, Response, HTTPException, Depends, File, UploadFile, Form
from users.repo import UsersRepo
from users.schemas import UserAdd, User, UserUpdate
from users.auth import get_password_hash, authenticate_user, create_access_token
from users.dependcies import get_current_user, get_current_superuser
from pydantic import EmailStr


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/signup")
async def create_user(user_data: UserAdd) -> dict:
    """ Create a new user """

    # check if the entered email already exists in the database
    existing_user = await UsersRepo.get_one(email=user_data.email.lower().strip())
    if existing_user:
        raise HTTPException(status_code=409, detail="Such a user already exists")

    hashed_password = get_password_hash(user_data.password.strip())
    await UsersRepo.set_one(
        email=user_data.email.lower().strip(),
        password=hashed_password,
        name=user_data.name.strip(),
        surname=user_data.surname.strip(),
        photo=user_data.photo
    )
    return {
        "email": user_data.email.lower().strip(),
        "name": user_data.name.strip(),
        "surname": user_data.surname.strip(),
        "photo": user_data.photo}


@router.post("/login")
async def login_user(response: Response, user_data: UserAdd) -> dict:
    """ Login user, use JWT access_token """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(401, detail="Incorrect name or password")
    else:
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie("parostok_access_token", access_token, httponly=True)

        return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response) -> dict:
    """ Logout the current user """
    response.delete_cookie("parostok_access_token")
    return {"logout": "ok"}


@router.get("/read")
async def read_user_info(current_user: User = Depends(get_current_user)) -> User:
    """ Get current user info """
    return current_user


# @router.post("/update_old")
# async def update_user_info(user_update: UserUpdate,
#                            current_user: User = Depends(get_current_user)) -> User:
#     """ Update current user info """
#
#     user = await UsersRepo.update_one(user_update, current_user)
#     return user

@router.post("/update")
async def update_user_info(
        name: str = Form(...),
        surname: str = Form(...),
        who_are_you: str = Form(...),
        image: Optional[UploadFile] = File(None),
        current_user: User = Depends(get_current_user)) -> User:
    """ Update current user info """

    photo = ""
    if image:
        # Uploading image file and getting the new filenames
        photo = await UsersRepo.add_image(image)

    if who_are_you:
        if who_are_you not in ['employee', 'employer']:
            raise HTTPException(400,
                                detail="Choose from the list ['employee', 'employer']")

    user_data = UserUpdate(
        name=name,
        surname=surname,
        who_are_you=who_are_you,
        photo=photo)

    user = await UsersRepo.update_one(user_data, current_user)
    return user


@router.post("/change")
async def change_email_password(
        email: str = Form(None),
        password: str = Form(None),
        current_user: UserAdd = Depends(get_current_user)) -> EmailStr:
    """ Update current user email, password """

    if email:
        # check if the entered email already exists in the database
        existing_user = await UsersRepo.get_one(email=email)
        if existing_user:
            raise HTTPException(status_code=409, detail="This email is already taken")
    else:
        email = current_user.email

    if password:
        hashed_password = get_password_hash(password)
    else:
        hashed_password = current_user.password

    user_data = UserAdd(
        email=email,
        password=hashed_password)

    await UsersRepo.update_one(user_data, current_user)
    return current_user.email


@router.get("/all")
async def get_all_users(current_user: User = Depends(get_current_superuser)) -> list[User]:
    """ Get all users, only for the superuser"""
    if current_user:
        users = await UsersRepo.get_all()
        return users


@router.get("/{user_id}")
async def get_user_id(user_id: int, user: User = Depends(get_current_superuser)) -> User:
    """ get information about the user by his user_id, only for the superuser """
    if user:
        user = await UsersRepo.get_by_id(user_id)  # get_by_id(1)
        return user


# @router.get("/{**kwargs}")
# async def get_user(**kwargs) -> User:
#     user = await UsersRepo.get_one(**kwargs)  # get_one(email="firm1@in.ua")
#     return user


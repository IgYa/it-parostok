from fastapi import APIRouter, Response, HTTPException, Depends
from users.repo import UsersRepo
from users.schemas import UserAdd, User, UserUpdate
from users.auth import get_password_hash, authenticate_user, create_access_token
from users.dependcies import get_current_user, get_current_superuser


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/signup")
async def create_user(user_data: UserAdd) -> dict:
    """ Create a new user """

    # check if the entered email already exists in the database
    existing_user = await UsersRepo.get_one(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Such a user already exists")

    hashed_password = get_password_hash(user_data.password)
    await UsersRepo.set_one(email=user_data.email, password=hashed_password)
    return {"message": "New user added"}


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


@router.post("/update")
async def update_user_info(user_update: UserUpdate,
                           current_user: User = Depends(get_current_user)) -> User:
    """ Update current user info """

    user = await UsersRepo.update_one(user_update, current_user)
    return user


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

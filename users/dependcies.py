from datetime import datetime
from fastapi import Request, HTTPException, Depends
from jose import JWTError, jwt
from config import ALGORITHM, AUTH_KEY
from users.repo import UsersRepo
from users.schemas import User, UserUpdate
from db import async_session


def get_token(request: Request):
    """ Get access a token from a cookie """
    token = request.cookies.get("parostok_access_token")
    if not token:
        raise HTTPException(401, detail="You are not logged in, no token")
    return token


async def get_current_user(token: str = Depends(get_token)):
    """ Decode the token,
        Check if the token has expired,
        Check if the user_id is in the token,
        Check if there is such a user in the database
        return user """
    try:
        payload = jwt.decode(token, AUTH_KEY, ALGORITHM)
    except JWTError:
        raise HTTPException(401, detail="You are not logged in, invalid token")

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(401, detail="You are not logged in, the token has expired")

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(401, detail="You are not logged in, no user_id")

    user = await UsersRepo.get_by_id(int(user_id))
    if not user:
        raise HTTPException(401, detail="You are not logged in, no such user is registered")

    return user


async def get_current_superuser(current_user: User = Depends(get_current_user)):
    """ Check if the user is a superuser """
    if not current_user.is_super:
        raise HTTPException(401, detail="You do not have superuser rights")
    return current_user


async def get_db():
    async with async_session() as session:
        yield session

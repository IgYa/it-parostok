from datetime import timedelta, datetime
from pydantic import EmailStr
from jose import jwt
from passlib.hash import pbkdf2_sha256
from users.repo import UsersRepo
from users.schemas import User
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, AUTH_KEY
from db import async_session

ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)


def verify_password(password, hashed_password) -> bool:
    """ Compare the entered password with the password hash stored in the database """
    return pbkdf2_sha256.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    """ Сounting hashed password """
    return pbkdf2_sha256.hash(password)


def create_access_token(data: dict) -> str:
    """ create access token """
    to_encode = data.copy()
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) + datetime.utcnow()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AUTH_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str) -> User:
    """ authenticate user, if Email, password match those stored in the database,
    return User and update Last Login-Time """

    user = await UsersRepo.get_one(email=email)
    if user and verify_password(password, user.password):
        # Update last_login
        user.last_login = datetime.utcnow()
        async with async_session() as ss:
            ss.add(user)
            await ss.commit()

        return user

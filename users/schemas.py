from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from typing import Optional, Literal
from datetime import datetime
from users.models import Role


class UserAdd(BaseModel):
    """ Validation scheme for adding a new user """
    email: EmailStr
    password: str
    name: Optional[str] = None
    surname: Optional[str] = None
    photo: Optional[str] = None


class UserUpdate(BaseModel):
    """ Validation scheme for updating a user """
    name: Optional[str] = None
    surname: Optional[str] = None
    occupation: Optional[str] = None
    company: Optional[str] = None
    photo: Optional[str] = None
    location: Optional[str] = None
    city: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
    # who_are_you: Optional[Literal["employee", "employer"]] = None

    # @field_validator("who_are_you", mode="before")
    # def convert_role_to_string(cls, value):
    #     if isinstance(value, Role):
    #         return value.value
    #     return value


class User(UserUpdate):
    """ Validation scheme for user """
    id: int
    email: EmailStr
    created_at: datetime
    last_login: Optional[datetime] = None

    # is_super: bool - this field is available only for the superuser
    # is_active: bool - this field is available only for the superuser


# class UserPasswordResetRequest(BaseModel):
#     """ Validation scheme for reset User's password - Request"""
#     email: EmailStr



# class UserPasswordReset(BaseModel):
#     """ Validation scheme for reset User's password - Response and Reset"""
#     token: str
#     new_password: str




# class UserId(BaseModel):
#     ok: bool = True
#     user_id: int



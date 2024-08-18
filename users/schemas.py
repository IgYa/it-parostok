from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from typing import Optional, Literal
from datetime import date, datetime
from users.models import Role


class UserAdd(BaseModel):
    """ Validation scheme for adding a new user """
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """ Validation scheme for updating a user """
    name: Optional[str] = None
    surname: Optional[str] = None
    who_are_you: Optional[Literal["employee", "employer"]] = None
    model_config = ConfigDict(from_attributes=True)

    @field_validator("who_are_you", mode="before")
    def convert_role_to_string(cls, value):
        if isinstance(value, Role):
            return value.value
        return value


class User(UserUpdate):
    """ Validation scheme for user """
    id: int
    email: EmailStr
    created_at: date
    last_login: Optional[datetime] = None
    photo_url: Optional[str] = None
    # is_super: bool - this field is available only for the superuser
    # is_active: bool - this field is available only for the superuser








# class UserId(BaseModel):
#     ok: bool = True
#     user_id: int



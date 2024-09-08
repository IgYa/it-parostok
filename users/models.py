from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import String, Enum, Boolean
from pydantic import EmailStr
from datetime import date, datetime
from enum import Enum as PyEnum
from db import Model, intpk, my_datetime


class Role(PyEnum):
    employee = "employee"
    employer = "employer"


class UserOrm(Model):
    """ User Model, tablename: "users"
    Attributes:
        id (int, primary_key): User ID
        email (EmailStr, NOT NULL): Email address, Unique field, identification of user by this field
        name (str): Username
        surname (str): User surname
        who_are_you(Role): User - "employee" or "employer"
        photo (str): names of the file for this user,
                     the file name is formed from the current date and time,
                     the files are stored in the folder static/images,
                     format "%Y%m%d_%H%M%S_%f".jpg, .png, .jpeg, .gif, .webp
        created_at (datetime): Date and time user was created, defaults to now
        last_login (datetime): Date and time last login of this user
        is_super: Whether this user is superuser, defaults to False
        is_active (bool): Whether this user is active, defaults to True
        """

    __tablename__ = "users"

    id: Mapped[intpk]
    email: Mapped[EmailStr] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[Optional[str]]
    surname: Mapped[Optional[str]]
    who_are_you: Mapped[Optional[Role]] = mapped_column(Enum(Role))
    photo: Mapped[Optional[str]]
    created_at: Mapped[my_datetime]
    last_login: Mapped[Optional[datetime]]
    is_super: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"

# Додамо зворотний зв'язок у модель UserOrm
UserOrm.project = relationship("ProjectOrm", back_populates="user")
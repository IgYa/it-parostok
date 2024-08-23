from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Boolean, JSON
from typing import List, Optional
from db import Model, intpk, my_datetime


class CategoriaOrm(Model):
    """Project Model, tablename: "projects"
    Attributes:
        id (int, primary_key):  Categoria ID
        name (str): Name of the  Categoria
        discription (str): Text of the  Categoria
        is_active (bool): Whether the project is published
        """
    __tablename__ = "categories"

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[Optional[str]]
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    # project = relationship("ProjectORM", back_populates="categoria")

    def __str__(self):
        return f"Categoria - {self.name}"


class ProjectOrm(Model):
    """Project Model, tablename: "projects"
    Attributes:
        id (int, primary_key): Project ID
        user_id (int): User ID (Foreign key, relationship to the users table, field -id)
        title (str): Name of the Project
        text (str): Text of the Project
        photos (List[str]): list with the names of the files for this project,
                            the file name is formed from the current date and time,
                            the files are stored in the folder static/images
        created_at (datetime): Date and time the project was created
        updated_at (datetime): Date and time of the last change
        is_active (bool): Whether the project is published
        """
    __tablename__ = "projects"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",
                                                    onupdate="RESTRICT",
                                                    ondelete="RESTRICT"))
    cat_id: Mapped[int] = mapped_column(ForeignKey("categories.id",
                                                    onupdate="RESTRICT",
                                                    ondelete="RESTRICT"))
    title: Mapped[str]
    text: Mapped[str]
    photos: Mapped[Optional[List[str]]] = mapped_column(JSON)
    created_at: Mapped[my_datetime]
    updated_at: Mapped[my_datetime]
        # onupdate=func.now(), onupdate=datetime.utcnow or create trigger
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    # Визначення зв'язку між ProjectOrm і UserOrm
    user = relationship("UserOrm", back_populates="project")
    categoria = relationship("CategoriaOrm", back_populates="project")

    def __str__(self):
        return f"Project #{self.id} - {self.title}"


# Додамо зворотний зв'язок у модель CategoriaOrm
CategoriaOrm.project = relationship("ProjectOrm", back_populates="categoria")
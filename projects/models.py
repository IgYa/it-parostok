from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Boolean, JSON, String
from typing import List, Optional
from db import Model, intpk, my_datetime, is_active, likes


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
    is_active: Mapped[is_active]

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
    views: Mapped[Optional[likes]]
    likes: Mapped[Optional[likes]]
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON)  # ["#Landscapes", "#Foto", "#Architecture"]
    contenttype: Mapped[Optional[str]]   # ["Photographs", "Video", "3D", "Drawings", "Vector"]
    orientation: Mapped[Optional[str]]  # ["Horizontal", "Vertical"]
    size: Mapped[Optional[str]]  # ["Large", "Medium", "Small"]
    colorscheme: Mapped[Optional[str]]  # ["Specific color", "Color", "Black and white"]
    popularity: Mapped[Optional[str]]  # ["Most liked", "Most commented", "Most viewed"]
    created_at: Mapped[my_datetime]
    updated_at: Mapped[my_datetime]
        # onupdate=func.now(), onupdate=datetime.utcnow or create trigger
    is_active: Mapped[is_active]

    # Визначення зв'язку між ProjectOrm і UserOrm
    user = relationship("UserOrm", back_populates="project")
    categoria = relationship("CategoriaOrm", back_populates="project")

    def __str__(self):
        return f"Project #{self.id} - {self.title}"


# Додамо зворотний зв'язок у модель CategoriaOrm
CategoriaOrm.project = relationship("ProjectOrm", back_populates="categoria")
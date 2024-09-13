from sqlalchemy import text

from db import async_session as session
from sqlalchemy import select, insert
from fastapi import UploadFile, HTTPException
from datetime import datetime
import os
from config import PATH_IMAGES
import aiofiles
from PIL import Image
from io import BytesIO


class BaseRepo:
    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        """ Get model data by model_id """
        async with session() as ss:
            query = select(cls.model).filter_by(id=model_id)
            result = await ss.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one(cls, **filter_by):
        """ Get model data by filter_by """
        async with session() as ss:
            query = select(cls.model).filter_by(**filter_by)
            result = await ss.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, **filter_by) -> list[model]:
        """ Get all model data """
        async with session() as ss:
            query = select(cls.model).filter_by(**filter_by)
            result = await ss.execute(query)
            return result.scalars().all()  # scalars() mappings() user_models =
            # user_schemas = [cls.model.model_validate(user_model) for user_model in user_models]
            # return user_schemas

    @classmethod
    async def set_one(cls, **data) -> None:
        """ Add a new model instance """
        async with session() as ss:
            query = insert(cls.model).values(**data)
            await ss.execute(query)
            await ss.commit()

    @staticmethod
    async def update_one(user_update, current_user):
        """ Update current model info """

        user_data = user_update.dict(exclude_unset=False)

        for key, value in user_data.items():
            setattr(current_user, key, value)

        async with session() as ss:
            ss.add(current_user)  # Додаємо об'єкт до сесії для відстеження змін
            await ss.commit()  # Зберігаємо зміни в базі даних
            await ss.refresh(current_user)  # Оновлюємо об'єкт current_user з бази даних

        return current_user

    @classmethod
    async def resize_image(cls, image: Image.Image, extension: str) -> bytes:
        """Resize the image to a maximum of 1920x1080"""
        MAX_WIDTH = 1920
        MAX_HEIGHT = 1080

        # Resize the image, maintaining the aspect ratio
        image.thumbnail((MAX_WIDTH, MAX_HEIGHT))

        # Save the resized image to a buffer
        buffer = BytesIO()
        if extension in [".jpg", ".jpeg"]:
            image.save(buffer, format="JPEG", quality=85)
        elif extension == ".png":
            image.save(buffer, format="PNG", optimize=True)
        elif extension == ".webp":
            image.save(buffer, format="WEBP", quality=85)
        else:
            image.save(buffer, format=image.format)  # Default save for other formats

        buffer.seek(0)
        return buffer.read()

    @classmethod
    async def add_image(cls, file: UploadFile) -> str:
        """ Add an image file to the Project and resize if it exceeds 2 MB"""

        MAX_FILE_SIZE = 2 * 1024 * 1024  # maximum image size - 2 Мб

        # Checking the file extension
        extension = os.path.splitext(file.filename)[1].lower()
        if extension not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            raise HTTPException(status_code=415, detail="Invalid file type")

        # Read the file content asynchronously
        content = await file.read()

        # Verify that the file is an image using Pillow
        try:
            image = Image.open(BytesIO(content))
            image.verify()
            image = Image.open(BytesIO(content))  # Reopen image for further processing
        except Exception:
            raise HTTPException(status_code=415, detail="Invalid image file")

        # If image size is greater than 2 MB, resize it
        if len(content) > MAX_FILE_SIZE:
            content = await cls.resize_image(image, extension)

        # Get the current date and time in the required format, form a new file name
        now = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        new_filename = f"{now}{extension}"
        path = f"{PATH_IMAGES}{new_filename}"

        # Use aiofiles for asynchronous file operations
        async with aiofiles.open(path, "wb") as buffer:
            await buffer.write(content)  # Write file content asynchronously

            # Перевірка чи файл дійсно збережений і не порожній
        file_size = os.path.getsize(path)
        if file_size == 0:
            raise HTTPException(status_code=500, detail="Saved file is empty")

        print(f"File {new_filename} saved successfully with size {file_size} bytes")

        return new_filename


    @staticmethod
    async def get_view(view) -> list[dict]:
        """ Get all model data """
        async with session() as ss:
            query = select(view)
            result = await ss.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_active_projects() -> list[dict]:
        # Робимо запит для отримання активних проектів
        async with session() as ss:
            sql = """
                SELECT 
                    p.id,
                    p.title,
                    p.text,
                    p.photos,
                    p.created_at,
                    p.updated_at,
                    CONCAT(u.name, ' ', u.surname) AS user_fullname,
                    c.name AS category_name
                FROM 
                    projects p
                JOIN 
                    users u ON p.user_id = u.id
                JOIN 
                    categories c ON p.cat_id = c.id
                WHERE 
                    p.is_active = true;
                """

            result = await ss.execute(text(sql))  # Асинхронне виконання запиту
            projects = result.mappings().all()  # Перетворення результату на відображення (mapping)

            return projects  #[dict(row) for row in projects]  # Перетворення в список словників

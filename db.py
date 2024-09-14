from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column
from config import *
from typing import Annotated
from sqlalchemy import func, TIMESTAMP, Boolean, Integer
from datetime import datetime


DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DB_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

intpk = Annotated[int, mapped_column(primary_key=True)]
my_datetime = Annotated[datetime, mapped_column(TIMESTAMP(timezone=False), server_default=func.now())]
is_active = Annotated[bool, mapped_column(Boolean, nullable=False, server_default="true")]
likes = Annotated[int, mapped_column(Integer, nullable=True)]


class Model(DeclarativeBase):
    pass

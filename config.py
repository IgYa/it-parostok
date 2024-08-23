from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")

AUTH_KEY = getenv("AUTH_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

PATH_IMAGES = getenv("PATH_IMAGES")

ADMIN_EMAIL = getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")


from pydantic import BaseModel


class EmailSettings(BaseModel):
    MAIL_USERNAME: str = "i24539008@gmail.com"
    MAIL_PASSWORD: str = "mnhs lchf nfhx uoqe"
    MAIL_FROM: str = "i24539008@gmail.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    MAIL_FROM_NAME: str = "Ihor"
    TEMPLATE_FOLDER: str = "front/templates"

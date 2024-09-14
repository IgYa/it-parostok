from sqladmin import ModelView
from users.models import UserOrm
from projects.models import ProjectOrm, CategoriaOrm
from markupsafe import Markup
from config import PATH_IMAGES


class UserAdmin(ModelView, model=UserOrm):
    column_list = [UserOrm.id, UserOrm.email, UserOrm.name, UserOrm.surname, UserOrm.photo]
    column_details_exclude_list = [UserOrm.password]
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    # Вказуємо, які поля показувати у формі редагування
    # form_columns = ["email", "name", "surname", "is_active"]
    # Вказуємо, які поля приховати у формі редагування
    form_excluded_columns = ["password", "created_at", "last_login"]


class ProjectAdmin(ModelView, model=ProjectOrm):
    column_list = [c.name for c in ProjectOrm.__table__.c] + [ProjectOrm.user]
    # column_details_exclude_list = [UserOrm.password]
    can_delete = False
    name = "Project"
    name_plural = "Projects"
    icon = "fa-solid fa-book"
    # Вказуємо, які поля приховати у формі редагування
    form_excluded_columns = ["user", "created_at", "updated_at"]


class CategoriaAdmin(ModelView, model=CategoriaOrm):
    column_list = [c.name for c in CategoriaOrm.__table__.c]
    # column_details_exclude_list = [UserOrm.password]
    can_delete = False
    name = "Categoria"
    name_plural = "Categories"
    icon = "fa-solid fa-book"
    # Вказуємо, які поля приховати у формі редагування
    # form_excluded_columns = ["user", "created_at", "updated_at"]


class ProjectView(ModelView, model=ProjectOrm):
    column_list = ["id", "title", "photos"]  # Перелік полів для відображення

    @staticmethod
    def _format_photos(self, model):
        # Форматування поля 'photos' для відображення мініатюр
        if model.photos:
            thumbnails = ''.join(
                f'<img src="{PATH_IMAGES}{photo}" width="100" height="100" style="margin-right: 10px;">'
                for photo in model.photos
            )
            return Markup(thumbnails)
        return ""

    column_formatters = {
        'photos': _format_photos,  # Застосування кастомного форматера до поля 'photos'
    }


class UserView(ModelView, model=UserOrm):
    column_list = ["id", "name", "surname", "photo"]  # Перелік полів для відображення

    @staticmethod
    def _format_photo(self, model):
        path = f"{PATH_IMAGES}{model.photo}"
        # Форматування поля 'photo' для відображення мініатюр
        if model.photo:
            thumbnails = f'<img src={path} width="100" height="100" style="margin-right: 10px;">'
            return Markup(thumbnails)
        return ""

    column_formatters = {
        'photo': _format_photo,  # Застосування кастомного форматера до поля 'photos'
    }
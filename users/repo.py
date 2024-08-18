from users.models import UserOrm
from baserepo import BaseRepo


class UsersRepo(BaseRepo):
    model = UserOrm

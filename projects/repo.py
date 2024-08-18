from projects.models import ProjectOrm
from baserepo import BaseRepo


class ProjectsRepo(BaseRepo):
    model = ProjectOrm

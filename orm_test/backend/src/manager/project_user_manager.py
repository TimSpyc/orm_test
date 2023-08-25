from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager
from datetime import datetime

class ProjectUserGroup(GroupTable):
    """
    A Django model representing a project user group, which associates a
    user with a project group.
    """
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    project_group = models.ForeignKey('ProjectGroup', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('user', 'project_group')

    def __str__(self):
        return f"{self.user} - {self.project_group}"

    @property
    def manager(self):
        return ProjectUserManager


class ProjectUser(DataTable):
    """
    A Django model representing a project user, including their project user
    group and project user roles.
    """
    project_user_group = models.ForeignKey(
        ProjectUserGroup,
        on_delete=models.DO_NOTHING
    )
    project_user_role = models.ManyToManyField('ProjectUserRole', blank=False)

    def __str__(self):
        return f'ProjectUser {self.id}'

    @property
    def group(self):
        return self.project_user_group

class ProjectUserManager(GeneralManager):

    group_model = ProjectUserGroup
    data_model = ProjectUser
    data_extension_model_list = []

    def __init__(
        self,
        project_user_group_id:int,
        search_date: datetime | None = None,
        use_cache: bool = True
    ):

        super().__init__(
            group_id=project_user_group_id,
            search_date=search_date,
            use_cache=use_cache
        )
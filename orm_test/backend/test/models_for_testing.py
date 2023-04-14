from backend.models import GroupTable, DataTable, ReferenceTable
from django.db import models

class TestProjectGroup(GroupTable):
    """
    A Django model representing a TestProject group.
    """
    def __str__(self):
        return f'{self.id}'

    class Meta:
        app_label = 'backend'

class TestProject(DataTable):
    """
    A Django model representing a TestProject, including its name, TestProject number, and associated TestProject group.
    """
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    project_group = models.ForeignKey(TestProjectGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'backend'

class TestProjectUserGroup(GroupTable):
    """
    A Django model representing a TestProject user group, which associates a user with a TestProject group.
    """
    def __str__(self):
        return f'{self.id}'

    class Meta:
        app_label = 'backend'


class TestProjectUserRole(ReferenceTable):
    """
    A Django model representing a TestProject user role, which includes a role name.
    """
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name

    class Meta:
        app_label = 'backend'


class TestProjectUser(DataTable):
    """
    A Django model representing a TestProject user, including their TestProject user group and TestProject user roles.
    """
    project_user_group = models.ForeignKey(TestProjectUserGroup, on_delete=models.CASCADE)
    project_user_role = models.ManyToManyField(TestProjectUserRole, blank=False)

    def __str__(self):
        return f'TestProjectUser {self.id}'

    class Meta:
        app_label = 'backend'
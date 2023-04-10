from django.db import models
from django.utils import timezone


class User(models.Model):
    microsoft_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class ProjectGroup(models.Model):

    def __str__(self):
        return self.id

class Project(models.Model):
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)
    active = models.BooleanField()

    def __str__(self):
        return self.name


class ProjectUserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project_group')

    def __str__(self):
        return f"{self.user} - {self.project_group}"


class ProjectUserRole(models.Model):
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name


class ProjectUser(models.Model):
    date = models.DateTimeField()
    project_user_group = models.ForeignKey(ProjectUserGroup, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    project_user_roles = models.ManyToManyField(ProjectUserRole, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'ProjectUser {self.id}'

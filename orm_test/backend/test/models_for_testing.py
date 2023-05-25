from datetime import datetime
from django.db import models

class TestProjectGroup(models.Model):
    """
    A Django model representing a TestProject group.
    """
    def __str__(self):
        return f'{self.id}'

    class Meta:
        app_label = 'backend'


class TestProject(models.Model):
    """
    A Django model representing a TestProject, including its name, TestProject number, and associated TestProject group.
    """
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    test_project_group = models.ForeignKey(TestProjectGroup, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False)

    def save(self,*args,**kwargs):
        if not self.date:
            self.date = datetime.now() 
        super().save(*args,**kwargs)    

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'backend'

class TestProjectUserGroup(models.Model):
    """
    A Django model representing a TestProject user group, which associates a user with a TestProject group.
    """
    def __str__(self):
        return f'{self.id}'

    class Meta:
        app_label = 'backend'


class TestProjectUserRole(models.Model):
    """
    A Django model representing a TestProject user role, which includes a role name.
    """
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name

    class Meta:
        app_label = 'backend'


class TestProjectUser(models.Model):
    """
    A Django model representing a TestProject user, including their TestProject user group and TestProject user roles.
    """
    test_project_user_group = models.ForeignKey(TestProjectUserGroup, on_delete=models.CASCADE)
    test_project_user_role = models.ManyToManyField(TestProjectUserRole, blank=False)

    def __str__(self):
        return f'TestProjectUser {self.id}'

    class Meta:
        app_label = 'backend'
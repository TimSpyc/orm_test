from datetime import datetime
from backend.src.auxiliary.manager import GeneralManager
from django.db import models
from backend.models import User
#from .models_for_testing import TestProjectGroup, TestProject, TestProjectUserGroup,TestProjectUser


class TestProjectGroup(models.Model):
    """
    A Django model representing a TestProject group.
    """
    def __str__(self):
        return f'{self.id}'

    class Meta:
        app_label = 'backend'


class TestProjectGroup2(models.Model):
    """
    A Django model representing a TestProject group.
    """
    unique1 = models.CharField(max_length=255)
    unique2 = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        unique_together = ('unique1', 'unique2')
        app_label = 'backend'

class TestProject3(models.Model):
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    test_project_group2 = models.ForeignKey(TestProjectGroup2, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, default=datetime.now())
    ap_no =models.IntegerField(null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    active = models.BooleanField(default = True)


    class Meta:
        unique_together = ('project_number', 'ap_no')
        app_label = 'backend'           

    def __str__(self):
        return self.name   

class TestProject(models.Model):
    """
    A Django model representing a TestProject, including its name, TestProject number, and associated TestProject group.
    """
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    test_project_group = models.ForeignKey(TestProjectGroup, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False, default=datetime.now())
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    active = models.BooleanField(default = True)

    class Meta:
        unique_together = ('project_number', 'test_project_group')
        app_label = 'backend'           

    def __str__(self):
        return self.name   
    

    
    
class TestProject2(models.Model):
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    test_project_group = models.ForeignKey(TestProjectGroup, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False, default=datetime.now())
    ap_no =models.IntegerField(null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    active = models.BooleanField(default = True)


    class Meta:
        unique_together = ('project_number', 'ap_no')
        app_label = 'backend'           

    def __str__(self):
        return self.name   


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
    date = models.DateTimeField(null=True, default=datetime.now())
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    active = models.BooleanField(default = True)


    def __str__(self):
        return f'TestProjectUser {self.id}'

    class Meta:
        app_label = 'backend'


class TestProjectUserGroup2(models.Model):
    unique1ProjectUserGroup = models.CharField(max_length=255)
    unique2ProjectUserGroup = models.CharField(max_length=255)

    def __str__(self):
      return f'{self.id}'
    class Meta:
        unique_together = ('unique1ProjectUserGroup', 'unique1ProjectUserGroup')
        app_label = 'backend'

class TestProjectUser2(models.Model):
    name = models.CharField(max_length=255)
    test_project_user_group2 = models.ForeignKey(TestProjectUserGroup2, on_delete=models.CASCADE)
    test_project_user_role = models.ManyToManyField(TestProjectUserRole,blank=False)
    date = models.DateTimeField(null=True, default=datetime.now())
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    active = models.BooleanField(default = True)
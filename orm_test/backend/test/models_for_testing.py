from datetime import datetime
from backend.src.auxiliary.manager import GeneralManager
from django.db import models
from backend.models import User



class TestGroupTable(models.Model):
    """
    An abstract Django model for representing group tables.
    """
    def getManager(
        self, 
        search_date: datetime, 
    ) -> GeneralManager:
        return self.manager(self.id, search_date)
    
    
    table_type = 'GroupTable'
    class Meta:
        abstract = True

class TestReferenceTable(models.Model):
    """
    An abstract Django model for representing reference tables.
    """
    active = models.BooleanField(default=True)
    table_type = 'ReferenceTable'
    class Meta:
        abstract = True

class TestDataTable(models.Model):
    """
    An abstract Django model for representing data tables, including date,
    creator, and active status.
    """
    date = models.DateTimeField()
    creator = models.ForeignKey("User", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    table_type = 'DataTable'
    class Meta:
        abstract = True

class TestDataExtensionTable(models.Model):
    """
    An abstract Django model for representing data extension tables.
    """
    table_type = 'DataExtensionTable'
    class Meta:
        abstract = True



class TestProjectGroup(TestGroupTable):
    """
    A Django model representing a TestProject group.
    """

    
    def __str__(self):
        return f'{self.id}'

    class Meta:
        app_label = 'backend'


class TestProjectGroup2(TestGroupTable):
    """
    A Django model representing a TestProject group.
    """
    unique1 = models.CharField(max_length=255)
    unique2 = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['unique1', 'unique2'],
                name='unique_test_project_group2'
            )
        ]
        app_label = 'backend'

class TestProject3(TestDataTable):
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    test_project_group2 = models.ForeignKey(TestProjectGroup2, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(null=True, default=datetime.now())
    ap_no =models.IntegerField(null=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null= True)
    active = models.BooleanField(default = True)

    @property
    def group_object(self):
        return self.test_project_group2
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project_number', 'ap_no'],
                name='unique_test_project3'
            )
        ]
        app_label = 'backend'           

    def __str__(self):
        return self.name   

class TestProject(TestDataTable):
    """
    A Django model representing a TestProject, including its name, TestProject number, and associated TestProject group.
    """
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    test_project_group = models.ForeignKey(TestProjectGroup, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(null=False, default=datetime.now())
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null= True)
    active = models.BooleanField(default = True)

    @property
    def group_object(self):
        return self.test_project_group

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project_number', 'test_project_group'],
                name='unique_test_project'
            )
        ]
        app_label = 'backend'           

    def __str__(self):
        return self.name   
    
class TestProject2(TestDataTable):
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    test_project_group = models.ForeignKey(TestProjectGroup, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(null=False, default=datetime.now())
    ap_no =models.IntegerField(null=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null= True)
    active = models.BooleanField(default = True)

    @property
    def group_object(self):
        return self.test_project_group
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project_number', 'ap_no'],
                name='unique_test_project2'
            )
        ]
        app_label = 'backend'           

    def __str__(self):
        return self.name   
    
class TestProjectGroup3(TestGroupTable):
    """
    A Django model representing a TestProject group.
    """
    unique3 = models.CharField(max_length=255)
    unique4 = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        app_label = 'backend'

class TestProjectUserGroup(TestGroupTable):
    """
    A Django model representing a TestProject user group, which associates a user with a TestProject group.
    """
    def __str__(self):
        return f'{self.id}'

    class Meta:
        app_label = 'backend'


class TestProjectUserRole(TestReferenceTable):
    """
    A Django model representing a TestProject user role, which includes a role name.
    """
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name

    class Meta:
        app_label = 'backend'


class TestProjectUser(TestDataTable):
    """
    A Django model representing a TestProject user, including their TestProject user group and TestProject user roles.
    """
    test_project_user_group = models.ForeignKey(TestProjectUserGroup, on_delete=models.DO_NOTHING)
    test_project_user_role = models.ManyToManyField(TestProjectUserRole, blank=False)
    date = models.DateTimeField(null=True, default=datetime.now())
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null= True)
    active = models.BooleanField(default = True)

    @property
    def group_object(self):
        return self.test_project_user_group

    def __str__(self):
        return f'TestProjectUser {self.id}'

    class Meta:
        app_label = 'backend'


class TestProjectUserGroup2(TestGroupTable):
    unique1ProjectUserGroup = models.CharField(max_length=255)
    unique2ProjectUserGroup = models.CharField(max_length=255)

    def __str__(self):
      return f'{self.id}'
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['unique1ProjectUserGroup', 'unique2ProjectUserGroup'],
                name='unique_test_project_user_group2'
            )
        ]
        app_label = 'backend'

class TestProjectUser2(models.Model):
    name = models.CharField(max_length=255)
    test_project_user_group2 = models.ForeignKey(TestProjectUserGroup2, on_delete=models.DO_NOTHING)
    test_project_user_role = models.ManyToManyField(TestProjectUserRole,blank=False)
    date = models.DateTimeField(null=True, default=datetime.now())
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    active = models.BooleanField(default = True)



class TestProject2ExtensionTable(TestDataExtensionTable):

    name_extension = models.CharField(max_length=255)
    price = models.IntegerField()
    test_project2 = models.ForeignKey(TestProject2, on_delete=models.CASCADE)

    @property
    def data_object(self):
        return self.test_project2







# TestProjectManager.create(
#     name='Test',
#     project_number='123'
#     TestProject2ExtensionTable=[{'name_extension': 1},{'name_extension': 2}]
# )

# TestProjectManager.update(
#     TestProject2ExtensionTable=[{'name_extension': 1},{'name_extension': 2}]
# )






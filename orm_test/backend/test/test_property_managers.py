from django.db import models
from backend.src.auxiliary.manager import GeneralManager
from backend.test.models_for_testing import TestDataTable, TestGroupTable, TestReferenceTable


class newAbcGroup(TestGroupTable):
    class Meta:
        app_label = 'backend'   

    @property
    def manager(self):
        return newAbcManager      

    
class newAbc(TestDataTable):
    name = models.CharField(max_length=255)
    new_abc_group = models.ForeignKey(newAbcGroup, on_delete=models.DO_NOTHING)
    
    @property
    def group_object(self):
        return self.new_abc_group
    
    class Meta:
        app_label = 'backend'           

    def __str__(self):
        return self.name
    
class newAbcManager(GeneralManager):
    group_model = newAbcGroup
    data_model = newAbc
    data_extension_model_list: list = []





    
class newKundenGroup(TestGroupTable):

    @property
    def manager(self):
        return newKundenManager
    class Meta:
        app_label = 'backend'           
 
    
class newKunden(TestDataTable):
    name = models.CharField(max_length=255)
    new_kunden_group = models.ForeignKey(newKundenGroup, on_delete=models.DO_NOTHING)
    
    @property
    def group_object(self):
        return self.new_kunden_group
    
    class Meta:
        app_label = 'backend'           

    def __str__(self):
        return self.name
    
class newKundenManager(GeneralManager):
    group_model = newKundenGroup
    data_model = newKunden
    data_extension_model_list: list = []


    



class newProjectGroup(TestGroupTable):
    new_abc_group = models.ForeignKey(newAbcGroup, on_delete=models.DO_NOTHING)

    @property
    def manager(self):
        return newProjectManager
    class Meta:
        app_label = 'backend'           

class newProject(TestDataTable):
    name = models.CharField(max_length=255)
    new_project_group = models.ForeignKey(newProjectGroup, on_delete=models.DO_NOTHING)
    new_kunden = models.ForeignKey(newKunden, on_delete=models.DO_NOTHING) ##refernce to data model of kundenManager
    
    @property
    def group_object(self):
        return self.new_project_group
    class Meta:
        app_label = 'backend'           

    def __str__(self):
        return self.name
    
class newProjectManager(GeneralManager):
    group_model = newProjectGroup
    data_model = newProject
    data_extension_model_list: list = []


class newProjectUserGroup(TestGroupTable):
    new_project_group = models.ForeignKey(newProjectGroup, on_delete=models.DO_NOTHING)
    @property
    def manager(self):
        return newProjectUserManager
    class Meta:
        app_label = 'backend'           

    
class newProjectUserRoles(TestReferenceTable):
    role = models.CharField(max_length=255)

    class Meta:
        app_label = 'backend'    

class newXyzGroup(TestGroupTable):
    @property
    def manager(self):
        return newXyzManager
    class Meta:
        app_label = 'backend'

class newXyz(TestDataTable):
    new_xyz_group = models.ForeignKey(newXyzGroup, on_delete=models.DO_NOTHING)
    
    @property
    def group_object(self):
        return self.new_xyz_group
    class Meta:
        app_label = 'backend'           


class newXyzManager(GeneralManager):
    group_model = newXyzGroup
    data_model = newXyz
    data_extension_model_list: list = []

class newProjectUser(TestDataTable):
    new_kunden = models.ForeignKey(newKunden, on_delete=models.DO_NOTHING, null=True)
    new_project_user_group = models.ForeignKey(newProjectUserGroup, on_delete=models.DO_NOTHING)
    new_project_user_role = models.ManyToManyField(newProjectUserRoles, blank=False)
    new_xyz = models.ManyToManyField(newXyz,null=True)
    
    @property
    def group_object(self):
        return self.new_project_user_group
    class Meta:
        app_label = 'backend'           

    
class newProjectUserManager(GeneralManager):
    group_model = newProjectUserGroup
    data_model = newProjectUser
    data_extension_model_list: list = []




    

  
    


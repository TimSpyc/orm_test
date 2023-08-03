from django.db import models
from backend.src.auxiliary.manager import GeneralManager
from backend.test.models_for_testing import TestDataTable, TestGroupTable, TestReferenceTable


class newAbcGroup(TestGroupTable):
    class Meta:
        app_label = 'backend'   

    def manager(self, search_date, use_cache):
        return newAbcManager(self.id, search_date, use_cache)        

    
class newAbc(TestDataTable):
    name = models.CharField(max_length=255)
    new_abc_group = models.ForeignKey(newAbcGroup, on_delete=models.DO_NOTHING)
    
    @property
    def group(self):
        return self.abc_group
    
    class Meta:
        app_label = 'backend'           

    def __str__(self):
        return self.name
    
class newAbcManager(GeneralManager):
    group_model = newAbcGroup
    data_model = newAbc
    data_extension_model_list: list = []

    def __init__(self, new_abc_group_id, search_date=None, use_cache=True):
        super().__init__(
            group_id=new_abc_group_id,
            search_date=search_date,
            use_cache=use_cache
            )    






    
class newKundenGroup(TestGroupTable):

    def manager(self, search_date, use_cache):
        return newKundenManager(self.id, search_date, use_cache)   
    class Meta:
        app_label = 'backend'           
 
    
class newKunden(TestDataTable):
    name = models.CharField(max_length=255)
    new_kunden_group = models.ForeignKey(newKundenGroup, on_delete=models.DO_NOTHING)
    
    @property
    def group(self):
        return self.new_kunden_group
    
    class Meta:
        app_label = 'backend'           

    def __str__(self):
        return self.name
    
class newKundenManager(GeneralManager):
    group_model = newKundenGroup
    data_model = newKunden
    data_extension_model_list: list = []

    def __init__(self, new_kunden_group_id, search_date=None, use_cache=True):
        super().__init__(
            group_id=new_kunden_group_id,
            search_date=search_date,
            use_cache=use_cache
            )


    



class newProjectGroup(TestGroupTable):
    new_abc_group = models.ForeignKey(newAbcGroup, on_delete=models.DO_NOTHING)

    
    def manager(self, search_date, use_cache):
        return newProjectManager(self.id, search_date, use_cache)  
    class Meta:
        app_label = 'backend'           

class newProject(TestDataTable):
    name = models.CharField(max_length=255)
    new_project_group = models.ForeignKey(newProjectGroup, on_delete=models.DO_NOTHING)
    new_kunden = models.ForeignKey(newKunden, on_delete=models.DO_NOTHING) ##refernce to data model of kundenManager
    
    @property
    def group(self):
        return self.new_project_group
    class Meta:
        app_label = 'backend'           

    def __str__(self):
        return self.name
    
class newProjectManager(GeneralManager):
    group_model = newProjectGroup
    data_model = newProject
    data_extension_model_list: list = []

    def __init__(self, new_project_group_id, search_date=None, use_cache=True):
        super().__init__(
            group_id=new_project_group_id,
            search_date=search_date,
            use_cache=use_cache
            )


class newProjectUserGroup(TestGroupTable):
    new_project_group = models.ForeignKey(newProjectGroup, on_delete=models.DO_NOTHING) 

    def manager(self, search_date, use_cache):
        return newProjectUserManager(self.id, search_date, use_cache) 
    class Meta:
        app_label = 'backend'           

    
class newProjectUserRoles(TestReferenceTable):
    role = models.CharField(max_length=255)

    class Meta:
        app_label = 'backend'    
    
class newProjectUser(TestDataTable):
    new_kunden = models.ForeignKey(newKunden, on_delete=models.DO_NOTHING, null=True) ##macht kein sinn weil ein kunde kann nicht beliebig viele projectuser haben
    new_project_user_group = models.ForeignKey(newProjectUserGroup, on_delete=models.DO_NOTHING)
    new_project_user_role = models.ManyToManyField(newProjectUserRoles, blank=False)
    
    @property
    def group(self):
        return self.new_project_user_group
    class Meta:
        app_label = 'backend'           

    
class newProjectUserManager(GeneralManager):
    group_model = newProjectUserGroup
    data_model = newProjectUser
    data_extension_model_list: list = []

    def __init__(self, new_project_user_group_id, search_date=None, use_cache=True):
        super().__init__(
            group_id=new_project_user_group_id,
            search_date=search_date,
            use_cache=use_cache
            )
        




    

  
    


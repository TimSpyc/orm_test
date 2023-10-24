from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class ProjectNumberGroup(GroupTable):
    """
    A Django model representing a project number group.
    """
    project_number = models.CharField(max_length=255, unique=False, null=True)

    def __str__(self):
        return f'Project_number_group {self.id}'

    @property
    def manager(self):
        return ProjectNumberManager

class ProjectNumber(DataTable):
    """
    A Django model representing a project number, including its network number
    and associated project number group.
    """ 
    project_number_group = \
        models.ForeignKey(ProjectNumberGroup, on_delete=models.DO_NOTHING)
    network_number = models.BigIntegerField(null=True)

    def __str__(self):
        return f'project_number {self.id}'
    
    @property
    def group_object(self):
        return self.project_number_group

class ProjectNumberManager(GeneralManager):
    """
    A manager class for handling ProjectNumber-related operations, extending 
    the GeneralManager.

    Attributes:
        group_model (models.Model): The ProjectNumberGroup model.
        data_model (models.Model): The ProjectNumber model.
    """
    group_model = ProjectNumberGroup
    data_model = ProjectNumber
    data_extension_models = []
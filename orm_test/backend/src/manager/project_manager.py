from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class ProjectGroup(GroupTable):
    """
    A Django model representing a project group.
    """

    @property
    def manager(self):
        return ProjectManager

    def __str__(self):
        return f'Project Group with {self.id}'


class Project(DataTable):
    """
    A Django model representing a project, including its name, project number,
    and associated project group.
    """
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    project_number_group = models.ForeignKey(
        'ProjectNumberGroup',
        on_delete=models.DO_NOTHING,
        null=True,
        default=None
    )
    project_status = models.ForeignKey(
        'ProjectStatus',
        on_delete=models.DO_NOTHING
    )
    project_type = models.ForeignKey('ProjectType', on_delete=models.DO_NOTHING)
    currency = models.ForeignKey('Currency', on_delete=models.DO_NOTHING)
    file_group = models.ForeignKey(
        'FileGroup',
        on_delete=models.DO_NOTHING,
        null=True,
        default=None
    )
    customer_group = models.ForeignKey(
        'CustomerGroup',
        on_delete=models.DO_NOTHING
    )
    probability_of_nomination = models.FloatField(null=True)


    @property
    def group_object(self):
        return self.project_group

    def __str__(self):
        return self.name



class ProjectManager(GeneralManager):
    """
    A manager class for handling Project-related operations, extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ProjectGroup model.
        data_model (models.Model): The Project model.
    """
    group_model = ProjectGroup
    data_model = Project
    data_extension_model_list = []

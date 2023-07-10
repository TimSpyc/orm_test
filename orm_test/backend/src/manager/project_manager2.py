from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager

class ProjectGroup(GroupTable):
    """
    A Django model representing a project group.
    """

    def manager(self, search_date, use_cache):
        return ProjectManager(self.id, search_date, use_cache)

    def __str__(self):
        return f'Project Group with {self.id}'


class Project(DataTable):
    """
    A Django model representing a project, including its name, project number,
    and associated project group.
    """
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False, null=True)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    @property
    def group(self):
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

    def __init__(self, project_group_id, search_date=None, use_cache=True):
        """
        Initialize a ProjectManager instance.

        Args:
            project_group_id (int): The ID of the ProjectGroup instance.
            search_date (datetime.datetime, optional): The date used for filtering data. Defaults to None.
            use_cache (bool, optional): Whether to use the cache for data retrieval. Defaults to True.
        """
        super().__init__(group_id=project_group_id, search_date=search_date, use_cache=use_cache)


def test():
    a = ProjectManager(1, use_cache=False)
    print(a.name)
    print(a.project_number)
    print(a.group_id)
    print(a.creator.first_name, a.creator.last_name)
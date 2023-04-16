if __name__ == '__main__':
    import sys
    import os

    sys.path.append(r'C:\Users\Spyc\Django_ORM')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\orm_test')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend\src\manager')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend\src\auxiliary')
    sys.path.append(r'C:\Users\Spyc\Django_ORM\orm_test\backend')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from backend.models import ProjectUserGroup, ProjectGroup, Project, User
from exceptions import NonExistentGroupError
from datetime import datetime
from manager import GeneralManager, updateCache

class ProjectManager(GeneralManager):
    """
    A manager class for handling Project-related operations, extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ProjectGroup model.
        data_model (models.Model): The Project model.
    """
    group_model = ProjectGroup
    data_model = Project

    def __init__(self, project_group_id, search_date=None, use_cache=True):
        """
        Initialize a ProjectManager instance.

        Args:
            project_group_id (int): The ID of the ProjectGroup instance.
            search_date (datetime.datetime, optional): The date used for filtering data. Defaults to None.
            use_cache (bool, optional): Whether to use the cache for data retrieval. Defaults to True.
        """
        project_group, project = super().__init__(
            group_id=project_group_id,
            search_date=search_date
        )

        self.name = project.name
        self.number = project.project_number

    @property
    def project_user_list(self):
        """
        Get a list of ProjectUserManager instances for the current ProjectManager.

        Returns:
            list: A list of ProjectUserManager instances.
        """
        from project_user_manager import ProjectUserManager
        return ProjectUserManager.filter(
            date=self.search_date,
            project_group_id=self.group_id
        )



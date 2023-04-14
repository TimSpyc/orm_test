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
from manager import GeneralManager, createCache, updateCache

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
            search_date=search_date,
            use_cache=use_cache
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


    # @classmethod
    # @createCache
    # def create(cls, project_number, project_name, creator_user_id):
    #     """Create a new ProjectManager instance with a new project.

    #     Keyword arguments:
    #     project_number -- The number of the new project
    #     project_name -- The name of the new project
    #     creator_user_id -- The ID of the user who created the project

    #     Returns: A new ProjectManager instance
    #     """

    #     project_group = ProjectGroup()
    #     project_group.save()

    #     new_project = Project(
    #         project_number=project_number,
    #         name=project_name,
    #         creator=User.objects.get(id=creator_user_id),
    #         date=datetime.now(),
    #         project_group=project_group,
    #         active=True
    #     )
    #     new_project.save()

    #     project_manager = cls(project_group.id)

    #     return project_manager

    # @updateCache
    # def deactivate(self):
    #     """Deactivate the current project by creating a new project instance with active set to False."""

    #     new_project = Project(
    #         project_number=self.number,
    #         name=self.name,
    #         creator=self.creator,
    #         date=datetime.now(),
    #         project_group_id=self.group_id,
    #         active=False
    #     )
    #     new_project.save()

    #     self.active = False

    # @updateCache
    # def update(self, project_number=None, name=None, creator_user_id=None):
    #     """Create a new project instance with updated information.

    #     Keyword arguments:
    #     project_number -- The updated project number (default None)
    #     name -- The updated project name (default None)
    #     creator_user_id -- The updated user ID (default None)
    #     """

    #     current_project = Project.objects.get(id=self.id)

    #     if project_number is None:
    #         project_number = current_project.project_number
    #     if name is None:
    #         name = current_project.name
    #     if creator_user_id is None:
    #         creator_user_id = current_project.creator.id

    #     new_project = Project(
    #         project_number=project_number,
    #         name=name,
    #         creator=User.objects.get(id=creator_user_id),
    #         date=datetime.now(),
    #         project_group=ProjectGroup.objects.get(id=self.group_id),
    #         active=True
    #     )
    #     new_project.save()

    #     self.id = new_project.id
    #     self.number = new_project.project_number
    #     self.name = new_project.name
    #     self.creator_user_id = new_project.creator.id
    #     self.date = new_project.date
    #     self.active = new_project.active

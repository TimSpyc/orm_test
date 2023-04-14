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

from backend.models import ProjectUserGroup, ProjectUser, User, ProjectUserRole
from datetime import datetime
from manager import GeneralManager


class ProjectUserManager(GeneralManager):
    """
    A manager class for handling ProjectUser-related operations, extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ProjectUserGroup model.
        data_model (models.Model): The ProjectUser model.
    """

    group_model = ProjectUserGroup
    data_model = ProjectUser

    def __init__(self, project_user_group_id, search_date=None, use_cache=True):
        """
        Initialize a ProjectUserManager instance.

        Args:
            project_user_group_id (int): The ID of the ProjectUserGroup instance.
            search_date (datetime.datetime, optional): The date used for filtering data. Defaults to None.
            use_cache (bool, optional): Whether to use the cache for data retrieval. Defaults to True.
        """

        project_user_group, project_user = super().__init__(
            group_id=project_user_group_id,
            search_date=search_date,
            use_cache=use_cache
        )

        self.project_group_id = project_user_group.project_group_id
        self.user_id = project_user_group.user_id
        self.user = project_user_group.user
        self.roles = [{"id": role.id, "name": role.role_name}
                      for role in project_user.project_user_roles.all()]

    @property
    def project_manager(self):
        """
        Get a ProjectManager instance for the current ProjectUserManager.

        Returns:
            ProjectManager: An instance of the ProjectManager class.
        """
        from project_manager import ProjectManager
        return ProjectManager(self.project_group_id, self.search_date)



from backend.models import ProjectUserGroup, ProjectUser
from backend.src.auxiliary.manager import GeneralManager
import timeit


class ProjectUserManager(GeneralManager):
    """
    A manager class for handling ProjectUser-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ProjectUserGroup model.
        data_model (models.Model): The ProjectUser model.
    """

    group_model = ProjectUserGroup
    data_model = ProjectUser

    def __init__(
            self, 
            project_user_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a ProjectUserManager instance.

        Args:
            project_user_group_id (int): The ID of the ProjectUserGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """

        project_user_group, project_user = super().__init__(
            group_id=project_user_group_id,
            search_date=search_date,
        )
        self.project_user_group = project_user_group.id
        self.project_group_id: int = project_user_group.project_group.id
        self.project_user_id: int = project_user_group.user.id
        self.project_user_role_list: list = [
            project_user_role for project_user_role in
            project_user.project_user_role.all()
        ]
       
 
    @property
    def project_manager(self):
        """
        Get a ProjectManager instance for the current ProjectUserManager.

        Returns:
            ProjectManager: An instance of the ProjectManager class.
        """
        from project_manager import ProjectManager
        return ProjectManager(self.project_group_id, self.search_date)

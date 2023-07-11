
from datetime import date
from backend.models import ProjectStaffCost, ProjectStaffCostGroup
from backend.src.auxiliary.manager import GeneralManager

class ProjectStaffCostManager(GeneralManager):
    """
    A manager class for handling ProjectStaffCost-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ProjectStaffCostGroup model.
        data_model (models.Model): The ProjectStaffCost model.
    """
    group_model = ProjectStaffCostGroup
    data_model = ProjectStaffCost

    def __init__(
            self, 
            project_staff_cost_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a ProjectStaffCostManager instance.

        Args:
            project_group_id (int): 
                The ID of the ProjectStaffCostGroup instance
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        project_staff_cost_group, project_staff_cost = super().__init__(
            group_id=project_staff_cost_group_id,
            search_date=search_date
        )

        self.project_group_: int = project_staff_cost_group.project_group.id
        self.project_staff_cost_task_id: int = \
            project_staff_cost_group.project_staff_cost_task.id
        self.work_date : date = project_staff_cost_group.work_date
        self.project_staff_cost_group = project_staff_cost_group.id
        self.hours: float = project_staff_cost.hours


    @property
    def project_manager(self):
        """
        Get a ProjectManager instance for the current ProjectStaffCostManager.

        Returns:
            ProjectManager: An instance of the ProjectManager class.
        """
        from project_manager import ProjectManager
        return ProjectManager(self.project_group_id, self.search_date)


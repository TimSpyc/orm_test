from backend.models import ChangeRequestFeasibility,ChangeRequestFeasibilityGroup
from backend.src.auxiliary.manager import GeneralManager


class ChangeRequestFeasibilityManager(GeneralManager):
    """
    A manager class for handling ChangeRequestFeasibility-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ChangeRequestFeasibilityGroup model.
        data_model (models.Model): The ChangeRequestFeasibility model.
    """
    group_model = ChangeRequestFeasibilityGroup
    data_model = ChangeRequestFeasibility

    def __init__(
            self, 
            change_request_feasibility_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a ChangeRequestFeasibilityManager instance.

        Args:
            change_request_feasibility_group_id (int): 
                The ID of the ChangeRequestFeasibilityGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        change_request_feasibility_group, change_request_feasibility = \
            super().__init__(
            group_id=change_request_feasibility_group_id,
            search_date=search_date
        )
        self.project_user_role_id: int = \
            change_request_feasibility_group.project_user_role.id
        self.change_request_group_id: int = \
            change_request_feasibility_group.change_request_group.id
        self.description = change_request_feasibility.description
        self.confirmed = change_request_feasibility.confirmed
        self.change_request_feasibility_group = \
            change_request_feasibility_group.id
        
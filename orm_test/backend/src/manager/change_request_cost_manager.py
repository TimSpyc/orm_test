from backend.models import ChangeRequestCost, ChangeRequestCostGroup
from backend.src.auxiliary.manager import GeneralManager


class ChangeRequestCostManager(GeneralManager):
    """
    A manager class for handling ChangeRequestCost-related operations,
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ChangeRequestCostGroup model.
        data_model (models.Model): The ChangeRequestCost model.
    """
    group_model = ChangeRequestCostGroup
    data_model = ChangeRequestCost

    def __init__(
            self, 
            change_request_cost_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a ChangeRequestCostManager instance.

        Args:
            change_request_cost_group_id (int): 
                The ID of the ChangeRequestCostGroup instance.
            search_date (datetime.datetime, optional): 
                 The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                 Whether to use the cache for data retrieval. Defaults to True.
        """
        change_request_cost_group, change_request_cost = super().__init__(
            group_id=change_request_cost_group_id,
            search_date=search_date
        )
        self.description = change_request_cost.description
        self.cost_estimation = change_request_cost.cost_estimation
        self.change_request_cost_group = change_request_cost_group.id

        self.project_user_role_id: int = \
        change_request_cost_group.project_user_role.id
        self.change_request_group_id: int = \
            change_request_cost_group.change_request_group.id
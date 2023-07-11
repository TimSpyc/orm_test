from backend.models import ChangeRequestRisk, ChangeRequestRiskGroup
from backend.src.auxiliary.manager import GeneralManager


class ChangeRequestRiskManager(GeneralManager):
    """
    A manager class for handling ChangeRequestRisk-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ChangeRequestRiskGroup model.
        data_model (models.Model): The ChangeRequestRisk model.
    """
    group_model = ChangeRequestRiskGroup
    data_model = ChangeRequestRisk

    def __init__(
            self, 
            change_request_risk_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a ChangeRequestRiskManager instance.

        Args:
            change_request_cost_group_id (int):
                 The ID of the ChangeRequestRiskGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        change_request_risk_group, change_request_risk = super().__init__(
            group_id=change_request_risk_group_id,
            search_date=search_date
        )
    
        self.change_request_risk_probability = \
            change_request_risk.change_request_risk_probability
        self.change_request_risk_impact = \
            change_request_risk.change_request_risk_impact
        self.description = change_request_risk.description
        self.feedback = change_request_risk.feedback
        self.next_step = change_request_risk.next_step
        self.change_request_risk_group = change_request_risk_group.id
        self.change_request_group_id: int = \
              change_request_risk_group.change_request_group.id
        self.project_user_role_id = \
              change_request_risk_group.project_user_role.id


# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable, ChangeRequestGroup
from backend.src.auxiliary.manager import GeneralManager

class ChangeRequestRiskGroup(GroupTable):
    """
    A Django model representing a change request risk group.
    """
    change_request_group = models.ForeignKey(
        ChangeRequestGroup, 
        on_delete=models.DO_NOTHING, 
    )
    project_user_role = models.ForeignKey(
        'ProjectUserRole', 
        on_delete=models.DO_NOTHING, 
    )

    def manager(self, search_date, use_cache):
        return ChangeRequestRiskManager(self.id, search_date, use_cache)
    
    class Meta:
        unique_together = (
            'change_request_group', 'project_user_role'
        )

    def __str__(self):
        return f'ChangeRequestRisk Group with id {self.id}'

class ChangeRequestRisk(DataTable):
    """
    A Django model representing a change request risk.
    """
    change_request_risk_group = models.ForeignKey(
        ChangeRequestRiskGroup, 
        on_delete=models.DO_NOTHING,
    )
    change_request_risk_category = models.ForeignKey(
        'ChangeRequestRiskCategory', 
        on_delete=models.DO_NOTHING,
    )
    change_request_risk_impact = models.ForeignKey(
        'ChangeRequestRiskImpact', 
        on_delete=models.DO_NOTHING,
    )
    change_request_risk_probability = models.ForeignKey(
        'ChangeRequestRiskProbability', 
        on_delete=models.DO_NOTHING,
    )
    description = models.TextField(blank=False, null=False)
    feedback = models.TextField(blank=True, null=True)
    next_step = models.TextField(blank=True, null=True)

    @property
    def group(self):
        return self.change_request_risk_group

    def __str__(self):
        return f'ChangeRequestRisk with id {self.id}'

class ChangeRequestRiskManager(GeneralManager):
    """
    A manager class for handling change request risk related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ChangeRequestRiskGroup model.
        data_model (models.Model): The ChangeRequestRisk model.
    """
    group_model = ChangeRequestRiskGroup
    data_model = ChangeRequestRisk
    data_extension_model_list = []

    def __init__(
        self, change_request_risk_group_id, search_date=None, use_cache=True
    ):
        """
        Initialize a ChangeRequestRiskManager instance.

        Args:
            change_request_risk_group_id (int): 
                The ID of the ChangeRequestRiskGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        super().__init__(
            group_id=change_request_risk_group_id, 
            search_date=search_date, 
            use_cache=use_cache
        )
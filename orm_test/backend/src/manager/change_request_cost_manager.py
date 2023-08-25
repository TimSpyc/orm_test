# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class ChangeRequestCostGroup(GroupTable):
    """
    A Django model representing a change request cost group.
    """
    change_request_group = models.ForeignKey(
        'ChangeRequestGroup', 
        on_delete=models.DO_NOTHING, 
    )
    project_user_role = models.ForeignKey(
        'ProjectUserRole', 
        on_delete=models.DO_NOTHING, 
    )

    def manager(self, search_date, use_cache):
        return ChangeRequestCostManager(self.id, search_date, use_cache)
    
    class Meta:
        unique_together = (
            'change_request_group', 'project_user_role'
        )

    def __str__(self):
        return f'ChangeRequestCost Group with id {self.id}'

class ChangeRequestCost(DataTable):
    """
    A Django model representing a change request cost.
    """
    change_request_cost_group = models.ForeignKey(
        ChangeRequestCostGroup, 
        on_delete=models.DO_NOTHING,
    )
    change_request_cost_category = models.ForeignKey(
        'ChangeRequestCostCategory', 
        on_delete=models.DO_NOTHING,
    )
    description = models.TextField(null=False)

    @property
    def group(self):
        return self.change_request_cost_group

    def __str__(self):
        return f'ChangeRequestCost with id {self.id}'

class ChangeRequestCostManager(GeneralManager):
    """
    A manager class for handling change request cost related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ChangeRequestCostGroup model.
        data_model (models.Model): The ChangeRequestCost model.
    """
    group_model = ChangeRequestCostGroup
    data_model = ChangeRequestCost
    data_extension_model_list = []

    def __init__(
        self, change_request_cost_group_id, search_date=None, use_cache=True
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
        super().__init__(
            group_id=change_request_cost_group_id, 
            search_date=search_date, 
            use_cache=use_cache
        )
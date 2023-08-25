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

    @property
    def manager(self):
        return ChangeRequestCostManager
    
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
    def group_object(self):
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
# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class ChangeRequestFeasibilityGroup(GroupTable):
    """
    A Django model representing a change request feasibility group.
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
        return ChangeRequestFeasibilityManager
    
    class Meta:
        unique_together = (
            'change_request_group', 'project_user_role'
        )

    def __str__(self):
        return f'ChangeRequestFeasibility Group with id {self.id}'

class ChangeRequestFeasibility(DataTable):
    """
    A Django model representing a change request feasibility.
    """
    change_request_feasibility_group = models.ForeignKey(
        ChangeRequestFeasibilityGroup, 
        on_delete=models.DO_NOTHING,
    )
    confirmed = models.BooleanField(null=False, default=False)
    description = models.TextField(null=False)

    @property
    def group(self):
        return self.change_request_feasibility_group

    def __str__(self):
        return f'ChangeRequestFeasibility with id {self.id}'

class ChangeRequestFeasibilityManager(GeneralManager):
    """
    A manager class for handling change request feasibility related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ChangeRequestFeasibilityGroup model.
        data_model (models.Model): The ChangeRequestFeasibility model.
    """
    group_model = ChangeRequestFeasibilityGroup
    data_model = ChangeRequestFeasibility
    data_extension_model_list = []

    def __init__(
        self, change_request_feasibility_group_id, search_date=None, use_cache=True
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
        super().__init__(
            group_id=change_request_feasibility_group_id, 
            search_date=search_date, 
            use_cache=use_cache
        )
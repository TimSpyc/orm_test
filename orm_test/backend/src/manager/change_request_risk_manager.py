# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class ChangeRequestRiskGroup(GroupTable):
    """
    A Django model representing a change request risk group.
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
        return ChangeRequestRiskManager
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['change_request_group', 'project_user_role'],
                name='unique_change_request_risk_group'
            )
        ]

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
    description = models.TextField(null=False)
    feedback = models.TextField(null=True)
    next_step = models.TextField(null=True)

    @property
    def group_object(self):
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
# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class AbsenceGroup(GroupTable):
    """
    A Django model representing a absence group.
    """
    absence_type = models.ForeignKey(
        'AbsenceType', 
        on_delete=models.DO_NOTHING, 
    )
    absence_start_date = models.DateTimeField()
    absence_end_date = models.DateTimeField()
    user = models.ForeignKey(
        'User', 
        on_delete=models.DO_NOTHING, 
    )

    @property
    def manager(self):
        return AbsenceManager
    
    class Meta:
        unique_together = (
            'absence_type', 'absence_start_date', 'absence_end_date', 'user'
        )

    def __str__(self):
        return f'Absence Group with id {self.id}'

class Absence(DataTable):
    """
    A Django model representing a absence.
    """
    absence_group = models.ForeignKey(AbsenceGroup, on_delete=models.DO_NOTHING)
    description = models.TextField(null=True)
    is_accepted = models.BooleanField(null=True)

    @property
    def group_object(self):
        return self.absence_group

    def __str__(self):
        return f'Absence with id {self.id}'

class AbsenceManager(GeneralManager):
    """
    A manager class for handling absence related operations, extending the 
    GeneralManager.

    Attributes:
        group_model (models.Model): The AbsenceGroup model.
        data_model (models.Model): The Absence model.
    """
    group_model = AbsenceGroup
    data_model = Absence
    data_extension_model_list = []
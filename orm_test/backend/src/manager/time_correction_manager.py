# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class TimeCorrectionGroup(GroupTable):
    """
    A Django model representing a time correction group.
    """
    user = models.ForeignKey(
        'User', 
        on_delete=models.DO_NOTHING, 
    )

    @property
    def manager(self):
        return TimeCorrectionManager

    def __str__(self):
        return f'TimeCorrection Group with id {self.id}'

class TimeCorrection(DataTable):
    """
    A Django model representing a time correction.
    """
    time_correction_group = models.ForeignKey(
        TimeCorrectionGroup, 
        on_delete=models.DO_NOTHING
    )
    time_correction_type = models.ForeignKey(
        'TimeCorrectionType', 
        on_delete=models.DO_NOTHING, 
    )
    time_correction_date = models.DateField()
    time_start_of_work = models.TimeField(null=True)
    time_start_of_lunch_break = models.TimeField(null=True)
    time_end_of_lunch_break = models.TimeField(null=True)
    time_end_of_work = models.TimeField(null=True)
    description = models.TextField(null=True)
    is_accepted = models.BooleanField(null=True)
    hash_code = models.CharField(max_length=255, null=True, unique=True)

    @property
    def group_object(self):
        return self.time_correction_group

    def __str__(self):
        return f'TimeCorrection with id {self.id}'

class TimeCorrectionManager(GeneralManager):
    """
    A manager class for handling time correction related operations, extending 
    the GeneralManager.

    Attributes:
        group_model (models.Model): The TimeCorrectionGroup model.
        data_model (models.Model): The TimeCorrection model.
    """
    group_model = TimeCorrectionGroup
    data_model = TimeCorrection
    data_extension_model_list = []
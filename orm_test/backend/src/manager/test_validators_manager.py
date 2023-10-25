# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

from backend.models.validators.date_validators import CompareDateTimeValidator

class TestManagerGroup(GroupTable):
    """
    ! Write your docstring here !
    """

    @property
    def manager(self):
        return TestManagerManager

    def __str__(self):
        return f'TestManager Group with id {self.id}'

class TestManager(DataTable):
    """
    ! Write your docstring here !
    """
    test_manager_group = models.ForeignKey(
        TestManagerGroup, 
        on_delete=models.DO_NOTHING
    )
    start_date = models.DateTimeField(null=True, default=None)
    end_date = models.DateTimeField(null=True, default=None)

    @property
    def custom_validator_list(self):
        return [
            CompareDateTimeValidator(self, "start_date", "end_date", "<")
        ]

    @property
    def group_object(self):
        return self.test_manager_group

    def __str__(self):
        return f'TestManager with id {self.id}'

class TestManagerManager(GeneralManager):
    """
    ! Write your docstring here !
    """
    group_model = TestManagerGroup
    data_model = TestManager
    data_extension_model_list = []
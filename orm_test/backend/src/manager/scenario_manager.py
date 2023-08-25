from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager
from datetime import datetime

class ScenarioGroup(GroupTable):
    """
    A Django model representing a scenario group.
    """
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.id

    @property
    def manager(self):
        return ScenarioManager

class Scenario(DataTable):
    """
    A Django model representing a scenario, including its name, data, and associated scenario group.
    """
    name = models.CharField(max_length=255)
    data = models.JSONField()

    def __str__(self):
        return self.name

    @property
    def group(self):
        return self.scenario_group

class ScenarioManager(GeneralManager):
    group_model = ScenarioGroup
    data_model = Scenario
    data_extension_models = []

    def __init__(self, scenario_group_id, search_date, use_cache):
        super().__init__(scenario_group_id, search_date, use_cache)
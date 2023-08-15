from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager
from datetime import datetime

class DerivativeConstelliumGroup(GroupTable):
    """
    A Django model representing a derivative Constellium group, which
    associates a derivative Constellium group with a project group.
    """
    project_group = models.ForeignKey('ProjectGroup', on_delete=models.DO_NOTHING)

    def manager(self, search_date, use_cache):
        return DerivativeConstelliumManager(self.id, search_date, use_cache)

    def __str__(self):
        return f"{self.id}"
    

class DerivativeConstellium(DataTable):
    """
    A Django model representing a derivative Constellium, including its name,
    start and end dates, derivative type, estimated price, estimated weight,
    and prediction accuracy.
    """
    derivative_constellium_group = models.ForeignKey(
        DerivativeConstelliumGroup,
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=255)
    derivative_type = models.ForeignKey(
        'DerivativeType',
        on_delete=models.DO_NOTHING
    )
    estimated_price = models.FloatField()
    estimated_weight = models.FloatField()
    prediction_accuracy = models.ForeignKey(
        'PredictionAccuracy',
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.name
    
    @property
    def group(self):
        return self.derivative_constellium_group


class DerivativeConstelliumDerivativeLmcConnection(DataExtensionTable):
    """
    A Django model representing a derivative Constellium derivative LMC
    connection, which associates a derivative Constellium with a derivative
    LMC.
    """
    derivative_constellium = models.ForeignKey(
        DerivativeConstellium,
        on_delete=models.DO_NOTHING
    )
    derivative_lmc = models.ForeignKey(
        'DerivativeLmcGroup',
        on_delete=models.DO_NOTHING
    )
    take_rate = models.FloatField()

    def __str__(self):
        return f"{self.derivative_constellium} - {self.derivative_lmc}"


class DerivativeConstelliumManager(GeneralManager):

    group_model = DerivativeConstelliumGroup
    data_model = DerivativeConstellium
    data_extension_model_list = []

    def __init__(
        self,
        derivative_constellium_group_id:int,
        search_date: datetime | None = None,
        use_cache: bool = True
    ):
        super().__init__(
            group_id=derivative_constellium_group_id,
            search_date=search_date,
            use_cache=use_cache
        )
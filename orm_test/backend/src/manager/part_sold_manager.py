from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager


class PartSoldGroup(GroupTable):
    """
    A Django model representing a part sold group.
    """
    part_recipient = models.ForeignKey('PartRecipientGroup', on_delete= models.DO_NOTHING)
    customer_part_number_sap = models.CharField(max_length=255)

    class Meta:
        unique_together = ('part_recipient', 'customer_part_number_sap')

    @property
    def manager(self):
        return PartSoldManager

    def __str__(self):
        return f"PartSoldGroup {self.id}"


class PartSold(DataTable):
    part_sold_group = models.ForeignKey(PartSoldGroup, on_delete= models.DO_NOTHING)
    sap_number = models.ForeignKey('SapNumber', on_delete= models.DO_NOTHING, null=True)
    customer_part_number = models.CharField(max_length=255)
    part_group = models.ManyToManyField('PartGroup',blank=True) 
    customer_group = models.ForeignKey('CustomerGroup', on_delete= models.DO_NOTHING)
    contract_group = models.ForeignKey('PartSoldContractGroup', on_delete= models.DO_NOTHING)
    currency = models.ForeignKey('Currency', on_delete= models.DO_NOTHING)
    description = models.TextField(null=True)
    validity_start_date = models.DateTimeField(null=True)
    validity_end_date = models.DateTimeField(null=True)
    cbd_date = models.DateTimeField()

    @property
    def group(self):
        return self.part_sold_group


class PartSoldPriceComponent(DataExtensionTable):
    part_sold = models.ForeignKey(PartSold, on_delete= models.DO_NOTHING)
    value = models.FloatField()
    saveable = models.BooleanField(default=False)
    part_sold_price_component_type = models.ForeignKey('PartSoldPriceComponentType', on_delete= models.DO_NOTHING)
    validity_start_date = models.DateTimeField(null=True)
    validity_end_date = models.DateTimeField(null=True)


class PartSoldMaterialPriceComponent(DataExtensionTable):
    part_sold = models.ForeignKey(PartSold, on_delete= models.DO_NOTHING)
    part_sold_material_price_type = models.ForeignKey('PartSoldMaterialPriceType', on_delete= models.DO_NOTHING)
    basis = models.FloatField()
    variable = models.BooleanField(default=True)
    use_gross_weight = models.BooleanField(default=False)
    current_saveable = models.BooleanField(default=False)
    basis_saveable = models.BooleanField(default=False)
    validity_start_date = models.DateTimeField(null=True)
    validity_end_date = models.DateTimeField(null=True)


class PartSoldMaterialWeight(DataExtensionTable):
    part_sold = models.ForeignKey(PartSold, on_delete= models.DO_NOTHING)
    part_sold_material_type = models.ForeignKey('MaterialType', on_delete= models.DO_NOTHING)
    gross_weight = models.FloatField()
    net_weight = models.FloatField()

    class Meta:
        unique_together = ('part_sold_material_type', 'part_sold')


class PartSoldSaving(DataExtensionTable):
    part_sold = models.ForeignKey(PartSold, on_delete= models.DO_NOTHING)
    saving_date = models.DateTimeField()
    saving_rate = models.FloatField()
    saving_unit = models.ForeignKey('SavingUnit', on_delete= models.DO_NOTHING)


class PartSoldManager(GeneralManager):
    """
    A manager class for handling PartSold-related operations, extending the GeneralManager.
    """
    group_model = PartSoldGroup
    data_model = PartSold
    data_extension_model_list = [
        PartSoldPriceComponent,
        PartSoldMaterialPriceComponent,
        PartSoldMaterialWeight,
        PartSoldSaving
    ]

    def __init__(self, project_group_id, search_date=None, use_cache=True):
        """
        Initialize a ProjectManager instance.

        Args:
            project_group_id (int): The ID of the ProjectGroup instance.
            search_date (datetime.datetime, optional): The date used for filtering data. Defaults to None.
            use_cache (bool, optional): Whether to use the cache for data retrieval. Defaults to True.
        """
        super().__init__(group_id=project_group_id, search_date=search_date, use_cache=use_cache)
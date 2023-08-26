# Responsible Maximilian Kelm
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class AssetItemGroup(GroupTable):
    """
    A Django model representing a asset item group.
    """

    @property
    def manager(self):
        return AssetItemManager

    def __str__(self):
        return f'Asset Item Group with id {self.id}'

class AssetItem(DataTable):
    """
    A Django model representing a asset item, including its name, max width, max
    height, description and associated asset item group.
    """
    temp_validators = [MinValueValidator(1), MaxValueValidator(3)]

    asset_item_group = models.ForeignKey(
        AssetItemGroup, 
        on_delete=models.DO_NOTHING,
    )
    name = models.CharField(max_length=150)
    max_width = models.PositiveSmallIntegerField(
        default=1, validators=temp_validators
    )
    max_height = models.PositiveSmallIntegerField(
        default=1, validators=temp_validators
    )
    description = models.TextField(null=True)

    @property
    def group_object(self):
        return self.asset_item_group

    def __str__(self):
        return f'Asset Item with id {self.id}'

class AssetItemManager(GeneralManager):
    """
    A manager class for handling asset item related operations, extending the 
    GeneralManager.

    Attributes:
        group_model (models.Model): The AssetItemGroup model.
        data_model (models.Model): The AssetItem model.
    """
    group_model = AssetItemGroup
    data_model = AssetItem
    data_extension_model_list = []
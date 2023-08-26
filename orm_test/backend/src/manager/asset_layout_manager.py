# Responsible Maximilian Kelm
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class AssetLayoutGroup(GroupTable):
    """
    A Django model representing a asset layout group, including the asset 
    item site connection group, user and grid size.
    """
    asset_item_site_connection_group = models.ForeignKey(
        'AssetItemSiteConnectionGroup', 
        on_delete=models.DO_NOTHING,
    )
    user = models.ForeignKey(
        'User', 
        on_delete=models.DO_NOTHING, 
    )
    grid_size = models.PositiveSmallIntegerField(
        default=3, validators=[MinValueValidator(1), MaxValueValidator(3)]
    )

    @property
    def manager(self):
        return AssetLayoutManager

    class Meta:
        unique_together = (
            'asset_item_site_connection_group', 
            'user', 
            'grid_size'
        )

    def __str__(self):
        return f'Asset Layout Group with id {self.id}'

class AssetLayout(DataTable):
    """
    A Django model representing a asset layout, including its height, width, 
    x coordinate, y coordinate and associated asset layout group.
    """
    temp_validators = [MinValueValidator(1), MaxValueValidator(3)]

    height = models.PositiveSmallIntegerField(default=1, validators=temp_validators)
    width = models.PositiveSmallIntegerField(default=1, validators=temp_validators)
    x_coordinate = models.PositiveSmallIntegerField(default=0)
    y_coordinate = models.PositiveSmallIntegerField(default=0)
    asset_layout_group = models.ForeignKey(
        AssetLayoutGroup, 
        on_delete=models.DO_NOTHING,
    )

    @property
    def group_object(self):
        return self.asset_layout_group

    def __str__(self):
        return f'Asset Layout with id {self.id}'

class AssetLayoutManager(GeneralManager):
    """
    A manager class for handling asset layout related operations, extending the 
    GeneralManager.

    Attributes:
        group_model (models.Model): The AssetLayoutGroup model.
        data_model (models.Model): The AssetLayout model.
    """
    group_model = AssetLayoutGroup
    data_model = AssetLayout
    data_extension_model_list = []
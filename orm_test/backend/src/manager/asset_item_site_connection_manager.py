# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class AssetItemSiteConnectionGroup(GroupTable):
    """
    A Django model representing a asset item site connection group, including 
    the asset site group and asset item group.
    """
    asset_site_group = models.ForeignKey(
        'AssetSiteGroup', 
        on_delete=models.DO_NOTHING,
    )
    asset_item_group = models.ForeignKey(
        'AssetItemGroup', 
        on_delete=models.DO_NOTHING,
    )

    @property
    def manager(self):
        return AssetItemSiteConnectionManager

    class Meta:
        unique_together = ('asset_site_group', 'asset_item_group')

    def __str__(self):
        return f'Asset Item Site Connection Group with id {self.id}'

class AssetItemSiteConnection(DataTable):
    """
    A Django model representing a asset item site connection, including the is
    released state and associated asset item site connection group.
    """
    asset_item_site_connection_group = models.ForeignKey(
        AssetItemSiteConnectionGroup, 
        on_delete=models.DO_NOTHING,
    )
    is_released = models.BooleanField(default=False)

    @property
    def group(self):
        return self.asset_item_site_connection_group

    def __str__(self):
        return f'Asset Item Site Connection with id {self.id}'

class AssetItemSiteConnectionManager(GeneralManager):
    """
    A manager class for handling asset item site connection related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The AssetItemSiteConnectionGroup model.
        data_model (models.Model): The AssetItemSiteConnection model.
    """
    group_model = AssetItemSiteConnectionGroup
    data_model = AssetItemSiteConnection
    data_extension_model_list = []

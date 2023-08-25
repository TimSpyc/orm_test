from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class AssetSiteGroup(GroupTable):
    """
    A Django model representing a asset site group.
    """

    @property
    def manager(self):
        return AssetSiteManager

    def __str__(self):
        return f'Asset Site Group with id {self.id}'

class AssetSite(DataTable):
    """
    A Django model representing a asset site, including its name and associated 
    asset site group.
    """
    asset_site_group = models.ForeignKey(
        AssetSiteGroup, 
        on_delete=models.DO_NOTHING,
    )
    name = models.CharField(max_length=150)

    @property
    def group(self):
        return self.asset_site_group

    def __str__(self):
        return self.name

class AssetSiteManager(GeneralManager):
    """
    A manager class for handling asset site related operations, extending the 
    GeneralManager.

    Attributes:
        group_model (models.Model): The AssetSiteGroup model.
        data_model (models.Model): The AssetSite model.
    """
    group_model = AssetSiteGroup
    data_model = AssetSite
    data_extension_model_list = []
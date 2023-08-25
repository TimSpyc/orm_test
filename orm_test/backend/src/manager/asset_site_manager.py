from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class AssetSiteGroup(GroupTable):
    """
    A Django model representing a asset site group.
    """
    def manager(self, search_date, use_cache):
        return AssetSiteManager(self.id, search_date, use_cache)

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
    A manager class for handling asset-site-related operations, extending the 
    GeneralManager.

    Attributes:
        group_model (models.Model): The AssetSiteGroup model.
        data_model (models.Model): The AssetSite model.
    """
    group_model = AssetSiteGroup
    data_model = AssetSite
    data_extension_model_list = []

    def __init__(
        self, asset_site_group_id, search_date=None, use_cache=True
    ):
        """
        Initialize a AssetSiteManager instance.

        Args:
            asset_site_group_id (int): 
                The ID of the AssetSiteGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        super().__init__(
            group_id=asset_site_group_id, 
            search_date=search_date, 
            use_cache=use_cache
        )
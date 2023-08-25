# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable, User, AssetItemSiteConnectionGroup
from backend.src.auxiliary.manager import GeneralManager

class PermissionMasterGroup(GroupTable):
    """
    A Django model representing a permission master group, including the asset 
    item site connection group and user.
    """
    asset_item_site_connection_group = models.ForeignKey(
        AssetItemSiteConnectionGroup, 
        on_delete=models.DO_NOTHING,
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING, 
    )

    def manager(self, search_date, use_cache):
        return PermissionMasterManager(self.id, search_date, use_cache)

    class Meta:
        unique_together = ('asset_item_site_connection_group', 'user')

    def __str__(self):
        return f'Permission Master Group with id {self.id}'

class PermissionMaster(DataTable):
    """
    A Django model representing a permission master, including its associated 
    permission master group.
    """
    permission_master_group = models.ForeignKey(
        PermissionMasterGroup, 
        on_delete=models.DO_NOTHING,
    )

    @property
    def group(self):
        return self.permission_master_group

    def __str__(self):
        return f'Permission Master with id {self.id}'

class PermissionMasterManager(GeneralManager):
    """
    A manager class for handling permission-master-related operations, extending 
    the GeneralManager.

    Attributes:
        group_model (models.Model): The PermissionMasterGroup model.
        data_model (models.Model): The PermissionMaster model.
    """
    group_model = PermissionMasterGroup
    data_model = PermissionMaster
    data_extension_model_list = []

    def __init__(
        self, permission_master_group_id, search_date=None, use_cache=True
    ):
        """
        Initialize a PermissionMasterManager instance.

        Args:
            permission_master_group_id (int): 
                The ID of the PermissionMasterGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        super().__init__(
            group_id=permission_master_group_id, 
            search_date=search_date, 
            use_cache=use_cache
        )
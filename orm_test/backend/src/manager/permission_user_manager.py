# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable, User, PermissionType, AssetItemSiteConnectionGroup
from backend.src.auxiliary.manager import GeneralManager

class PermissionUserGroup(GroupTable):
    """
    A Django model representing a permission user group, including the asset 
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
        return PermissionUserManager(self.id, search_date, use_cache)

    class Meta:
        unique_together = ('asset_item_site_connection_group', 'user')

    def __str__(self):
        return f'Permission User Group with id {self.id}'

class PermissionUser(DataTable):
    """
    A Django model representing a permission user, including its type, 
    is_accepted state and associated permission user group.
    """
    permission_user_group = models.ForeignKey(
        PermissionUserGroup, 
        on_delete=models.DO_NOTHING,
    )
    permission_type = models.ForeignKey(
        PermissionType, 
        on_delete=models.DO_NOTHING,
    )
    is_accepted = models.BooleanField(null=True)

    @property
    def group(self):
        return self.permission_user_group

    def __str__(self):
        return f'Permission User with id {self.id}'

class PermissionUserManager(GeneralManager):
    """
    A manager class for handling permission user related operations, extending 
    the GeneralManager.

    Attributes:
        group_model (models.Model): The PermissionUserGroup model.
        data_model (models.Model): The PermissionUser model.
    """
    group_model = PermissionUserGroup
    data_model = PermissionUser
    data_extension_model_list = []

    def __init__(self, permission_user_group_id, search_date=None, use_cache=True):
        """
        Initialize a PermissionUserManager instance.

        Args:
            permission_user_group_id (int): 
                The ID of the PermissionUserGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                sWhether to use the cache for data retrieval. Defaults to True.
        """
        super().__init__(
            group_id=permission_user_group_id, 
            search_date=search_date, 
            use_cache=use_cache
        )
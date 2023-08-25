# Responsible Maximilian Kelm
from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class ChangeRequestFileGroup(GroupTable):
    """
    A Django model representing a change request file group.
    """
    change_request_group = models.ForeignKey(
        'ChangeRequestGroup', 
        on_delete=models.DO_NOTHING, 
    )    
    file_group = models.ForeignKey(
        'FileGroup', 
        on_delete=models.DO_NOTHING,
    )

    def manager(self, search_date, use_cache):
        return ChangeRequestFileManager(self.id, search_date, use_cache)
    
    class Meta:
        unique_together = (
            'change_request_group', 'file_group'
        )

    def __str__(self):
        return f'ChangeRequestFile Group with id {self.id}'

class ChangeRequestFile(DataTable):
    """
    A Django model representing a change request file.
    """
    change_request_file_group = models.ForeignKey(
        ChangeRequestFileGroup, 
        on_delete=models.DO_NOTHING,
    )
    description = models.TextField(null=True)

    @property
    def group(self):
        return self.change_request_file_group

    def __str__(self):
        return f'ChangeRequestFile with id {self.id}'

class ChangeRequestFileManager(GeneralManager):
    """
    A manager class for handling change request file related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ChangeRequestFileGroup model.
        data_model (models.Model): The ChangeRequestFile model.
    """
    group_model = ChangeRequestFileGroup
    data_model = ChangeRequestFile
    data_extension_model_list = []

    def __init__(
        self, change_request_file_group_id, search_date=None, use_cache=True
    ):
        """
        Initialize a ChangeRequestFileManager instance.

        Args:
            change_request_file_group_id (int): 
                The ID of the ChangeRequestFileGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        super().__init__(
            group_id=change_request_file_group_id, 
            search_date=search_date, 
            use_cache=use_cache
        )
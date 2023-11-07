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

    @property
    def manager(self):
        return ChangeRequestFileManager
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['change_request_group', 'file_group'],
                name='unique_change_request_file_group'
            )
        ]

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
    def group_object(self):
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
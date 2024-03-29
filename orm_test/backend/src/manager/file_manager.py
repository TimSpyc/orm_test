from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager
from datetime import datetime

class FileGroup(GroupTable):
    """
    A Django model representing a file group, which associates a file group
    with a project group.
    """

    @property
    def manager(self):
        return FileManager

    def __str__(self):
        return f"{self.id}"

class File(DataTable):
    """
    A Django model representing a file, including its name, start and end
    dates, file type, estimated price, estimated weight, and prediction
    accuracy.
    """
    file_group = models.ForeignKey(
        FileGroup,
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=255)
    file_type = models.ForeignKey(
        'FileType',
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.name
    
    @property
    def group_object(self):
        return self.file_group
    

class FileManager(GeneralManager):

    group_model = FileGroup
    data_model = File
    data_extension_model_list = []
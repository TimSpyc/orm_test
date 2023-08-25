from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager
from datetime import datetime

class FileGroup(GroupTable):
    """
    A Django model representing a file group, which associates a file group
    with a project group.
    """

    def manager(self, search_date, use_cache):
        return FileManager(self.id, search_date, use_cache)

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
    def group(self):
        return self.file_group
    

class FileManager(GeneralManager):

    group_model = FileGroup
    data_model = File
    data_extension_model_list = []

    def __init__(
        self,
        file_group_id:int,
        search_date: datetime | None = None,
        use_cache: bool = True
    ):
        super().__init__(
            group_id=file_group_id,
            search_date=search_date,
            use_cache=use_cache
        )
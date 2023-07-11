from backend.models import File, FileGroup
from datetime import datetime
from backend.src.auxiliary.manager import GeneralManager

class FileManager(GeneralManager):
    """
    A manager class for handling Project-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The FileGroup model.
        data_model (models.Model): The File model.
    """
    group_model = FileGroup
    data_model = File

    def __init__(self, file_group_id, search_date=None, use_cache=True):
        """
        Initialize a FileManager instance.

        Args:
            file_group_id (int): The ID of the FileGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        file_group, file = super().__init__(
            group_id=file_group_id,
            search_date=search_date
        )
        self.file_type = file.file_type
        self.data = file.data
        self.name = file_group.name
        self.file_group = file_group.id

    
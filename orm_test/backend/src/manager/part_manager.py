from backend.models import Part, PartGroup
from backend.src.auxiliary.manager import GeneralManager

class PartManager(GeneralManager):
    """
    A manager class for handling Part-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PartGroup model.
        data_model (models.Model): The Part model.
    """
    group_model = PartGroup
    data_model = Part

    def __init__(self, part_group_id, search_date=None, use_cache=True):
        """
        Initialize a ContractManager instance.

        Args:
            part_group_id (int): The ID of the PartGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        part_group, part = super().__init__(
            group_id=part_group_id,
            search_date=search_date
        )
        self.part_group = part_group.id
      

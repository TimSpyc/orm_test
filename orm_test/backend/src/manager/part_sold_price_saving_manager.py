from backend.models import PartSoldPriceSaving, PartSoldPriceSavingGroup
from backend.src.auxiliary.manager import GeneralManager

class PartSoldPriceSavingManager(GeneralManager):
    """
    A manager class for handling PartSoldPriceSaving-related operations,extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PartSoldPriceSavingGroup model.
        data_model (models.Model): The PartSoldPriceSaving model.
    """
    group_model = PartSoldPriceSavingGroup
    data_model = PartSoldPriceSaving

    def __init__(self, part_sold_price_saving_group_id, search_date=None, use_cache=True):
        """
        Initialize a ContractManager instance.

        Args:
            part_sold_price_saving_group_id (int): 
                The ID of the PartSoldPriceSavingGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        part_sold_price_saving_group, part_sold_price_saving = super().__init__(
            group_id=part_sold_price_saving_group_id,
            search_date=search_date
        )
        self.part_sold_id: int = part_sold_price_saving_group.part_sold.id
        self.saving_date = part_sold_price_saving_group.saving_date
        self.saving_rate= part_sold_price_saving.saving_rate
        self.saving_unit = part_sold_price_saving.saving_unit
        self.part_sold_price_saving_group = part_sold_price_saving_group.id

    
    @property
    def part_sold(self):
        """
        Get a PartSold instance for the current PartSoldPriceSavingManager.

        Returns:
           PartSoldManager: An instance of the PartSoldManager class.
        """
        from part_sold_manager import PartSoldManager
        return PartSoldManager(self.part_sold_group_id, self.search_date) 
    

    @part_sold.setter
    def part_sold(self, value):
        """
        Set the part_sold property.

        Args:
            value (PartSold): The PartSold instance to set.
        """
        self._part_sold = value
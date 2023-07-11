from backend.models import PartSoldPrice, PartSoldPriceGroup
from backend.src.auxiliary.manager import GeneralManager

class PartSoldPriceManager(GeneralManager):
    """
    A manager class for handling PartSoldPrice-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PartSoldPriceGroup model.
        data_model (models.Model): The PartSoldPrice model.
    """
    group_model = PartSoldPriceGroup
    data_model = PartSoldPrice

    def __init__(
            self, 
            part_sold_price_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a ContractManager instance.

        Args:
            part_sold_price_group_id (int): 
                The ID of the PartSoldPriceGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        part_sold_price_group, part_sold_price = super().__init__(
            group_id=part_sold_price_group_id,
            search_date=search_date
        )
        self.part_sold_id: int = part_sold_price_group.part_sold.id
        self.part_sold_price_type = part_sold_price_group.part_sold_price_type
        self.part_sold_price_group = part_sold_price_group.id
        self.value = part_sold_price.value
        self.saveable = part_sold_price.saveable


    @property
    def part_sold(self):
        """
        Get a PartSold instance for the current PartSoldPriceManager.

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
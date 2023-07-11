from backend.models import PartSoldCustomerPrice, PartSoldCustomerPriceGroup
from backend.src.auxiliary.manager import GeneralManager

class PartSoldCustomerPriceManager(GeneralManager):
    """
    A manager class for handling PartSoldCustomerPrice-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PartSoldCustomerPriceGroup model.
        data_model (models.Model): The PartSoldCustomerPrice model.
    """
    group_model = PartSoldCustomerPriceGroup
    data_model = PartSoldCustomerPrice

    def __init__(
            self, 
            part_sold_customer_price_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a ContractManager instance.

        Args:
            part_sold_price_group_id (int): 
                The ID of the PartSoldGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        part_sold_customer_price_group, part_sold_customer_price = \
            super().__init__(
            group_id=part_sold_customer_price_group_id,
            search_date=search_date
        )
        self.part_sold_id: int = part_sold_customer_price_group.part_sold.id
        self.part_sold_price_type = \
            part_sold_customer_price_group.part_sold_price_type 
        self.price_date = part_sold_customer_price_group.price_date
        self.value = part_sold_customer_price.value
        self.part_sold_customer_price_group = part_sold_customer_price_group.id


    @property
    def part(self):
        """
        Get a PartGroup instance for the current PartSoldCustomerPriceManager.

        Returns:
            PartManager: An instance of the PartManager class.
        """
        from part_manager import PartManager
        return PartManager(self.part_group_id, self.search_date)  
    
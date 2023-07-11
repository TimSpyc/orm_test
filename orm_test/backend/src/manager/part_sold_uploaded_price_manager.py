from backend.models import PartSoldUploadedPrice, PartSoldUploadedPriceGroup
from backend.src.auxiliary.manager import GeneralManager

class PartSoldUploadedPriceManager(GeneralManager):
    """
    A manager class for handling PartSoldUploadedPrice-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PartSoldUploadedPriceGroup model.
        data_model (models.Model): The PartSoldUploadedPrice model.
    """
    group_model = PartSoldUploadedPriceGroup
    data_model = PartSoldUploadedPrice

    def __init__(
            self, 
            part_sold_uploaded_price_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a ContractManager instance.

        Args:
            part_sold_uploaded_price_group_id (int): 
                The ID of the PartSoldUploadedPriceGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        part_sold_uploaded_price_group, part_sold_uploaded_price = \
            super().__init__(
            group_id=part_sold_uploaded_price_group_id,
            search_date=search_date
        )
        self.part_sold_id: int = part_sold_uploaded_price_group.id
        self.validity_start_date = \
            part_sold_uploaded_price_group.validity_start_date
        self.part_sold_uploaded_price_group = part_sold_uploaded_price_group.id
        self.value = part_sold_uploaded_price.value
        self.lme_basis = part_sold_uploaded_price.lme_basis
        self.ecdp_basis = part_sold_uploaded_price.ecdp_basis
        self.billet_basis = part_sold_uploaded_price.billet_basis
        self.source = part_sold_uploaded_price.source
        self.description = part_sold_uploaded_price.description


    @property
    def part_sold(self):
        """
        Get a PartSold instance for the current PartSoldUploadedPriceManager.

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
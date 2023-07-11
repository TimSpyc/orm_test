from backend.models import PartSoldMaterialPrice, PartSoldMaterialPriceGroup
from backend.src.auxiliary.manager import GeneralManager

class PartSoldMaterialPriceManager(GeneralManager):
    """
    A manager class for handling PartSoldMaterialPrice-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PartSoldMaterialPriceGroup model.
        data_model (models.Model): The PartSoldMaterialPrice model.
    """
    group_model = PartSoldMaterialPriceGroup
    data_model = PartSoldMaterialPrice

    def __init__(
            self, 
            part_sold_material_price_group_id, 
            search_date=None, 
            use_cache=True
            ):
        """
        Initialize a ContractManager instance.

        Args:
            part_sold_uploaded_price_group_id (int): 
                The ID of the PartSoldMaterialPriceGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        part_sold_material_price_group, part_sold_material_price = \
            super().__init__(
            group_id=part_sold_material_price_group_id,
            search_date=search_date
        )
        self.part_sold_id: int = part_sold_material_price_group.part_sold.id
        self.part_sold_material_price_type = \
            part_sold_material_price_group.part_sold_material_price_type
        self.part_sold_material_price_group= part_sold_material_price_group.id
        self.variable = part_sold_material_price.variable
        self.basis = part_sold_material_price.basis
        self.use_gross_weight = part_sold_material_price.use_gross_weight
        self.saveable = part_sold_material_price.saveable

    @property
    def part_sold(self):
        """
        Get a PartSold instance for the current PartSoldMaterialPriceManager.

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
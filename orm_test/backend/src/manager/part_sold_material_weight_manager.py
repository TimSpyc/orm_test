from backend.models import PartSoldMaterialWeight, PartSoldMaterialWeightGroup
from backend.src.auxiliary.manager import GeneralManager

class PartSoldMaterialWeightManager(GeneralManager):
    """
    A manager class for handling PartSoldMaterialWeight-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PartSoldMaterialWeightGroup model.
        data_model (models.Model): The PartSoldMaterialWeight model.
    """
    group_model = PartSoldMaterialWeightGroup
    data_model = PartSoldMaterialWeight

    def __init__(
            self, 
            part_sold_material_weight_group_id, 
            search_date=None, 
            use_cache=True):
        """
        Initialize a ContractManager instance.

        Args:
            part_sold_material_weight_group_id (int): 
                The ID of the PartSoldMaterialWeightGroup instance.
            search_date (datetime.datetime, optional): 
                The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        part_sold_material_weight_group, part_sold_material_weight = \
            super().__init__(
            group_id=part_sold_material_weight_group_id,
            search_date=search_date
        )
        self.part_sold_id: int = part_sold_material_weight_group.part_sold.id
        self.part_sold_material_type = \
            part_sold_material_weight_group.part_sold_material_type
        self.gross_weight = part_sold_material_weight.gross_weight
        self.net_weight = part_sold_material_weight.net_weight
        self.part_sold_material_weight_group = part_sold_material_weight_group.id


    @property
    def part_sold(self):
        """
        Get a PartSold instance for the current PartSoldMaterialWeightManager.

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
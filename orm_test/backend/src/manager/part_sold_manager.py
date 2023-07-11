from backend.models import PartSold, PartSoldGroup
from backend.src.auxiliary.manager import GeneralManager

class PartSoldManager(GeneralManager):
    """
    A manager class for handling PartSold-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The PartSoldGroup model.
        data_model (models.Model): The PartSold model.
    """
    group_model = PartSoldGroup
    data_model = PartSold

    def __init__(self, part_sold_group_id, search_date=None, use_cache=True):
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
        part_sold_group, part_sold = super().__init__(
            group_id=part_sold_group_id,
            search_date=search_date
        )
        self.part_recipient = part_sold_group.part_recipient
        self.customer_part_number_sap = \
            part_sold_group.customer_part_number_sap
        self.sap_number = part_sold.sap_number
        self.part_sold_group = part_sold_group.id
        self.customer_part_number = part_sold.customer_part_number
        self.customer_plant = part_sold.customer_plant
        self.contract_group = part_sold.contract_group
        self.currency = part_sold.currency
        self.description = part_sold.description
        self.validity_start_date = part_sold.validity_start_date
        self.validity_end_date = part_sold.validity_end_date
        self.cbd_date = part_sold.cbd_date
        self.part_group_list: list = [
           part_group.id for part_group in
           part_sold.part_group.all()
       ]



    @property
    def part_manager_list(self):
        from part_manager import PartManager
        return [
            PartManager(part_group_id, self.search_date)
            for part_group_id in self.part_group_id_list
        ]

    @property
    def part(self):
        """
        Get a PartGroup instance for the current PartSoldManager.

        Returns:
            PartManager: An instance of the PartManager class.
        """
        from part_manager import PartManager
        return PartManager(self.part_group_id, self.search_date)  
    
    
    @property
    def contract(self):
        """
        Get a Contract instance for the current ContractManager.

        Returns:
            ContractManager: An instance of the ContractManager class.
        """
        from contract_manager import ContractManager
        return ContractManager(self.contract_group_id, self.search_date)  

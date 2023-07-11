from backend.models import Contract, ContractGroup
from backend.src.auxiliary.manager import GeneralManager, updateCache

class ContractManager(GeneralManager):
    """
    A manager class for handling Contract-related operations, 
    extending the GeneralManager.

    Attributes:
        group_model (models.Model): The ContractGroup model.
        data_model (models.Model): The Contract model.
    """
    group_model = ContractGroup
    data_model = Contract

    def __init__(self, contract_group_id, search_date=None, use_cache=True):
        """
        Initialize a ContractManager instance.

        Args:
            contract_group_id (int): The ID of the ContractGroup instance.
            search_date (datetime.datetime, optional):
                 The date used for filtering data. Defaults to None.
            use_cache (bool, optional): 
                Whether to use the cache for data retrieval. Defaults to True.
        """
        contract_group, contract = super().__init__(
            group_id=contract_group_id,
            search_date=search_date
        )
        self.description = contract.description
        self.contract_date = contract_group.date
        self.contract_number = contract_group.contract_number
        self.contract_group = contract_group.id
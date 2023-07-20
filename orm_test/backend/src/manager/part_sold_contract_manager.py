from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager

class PartSoldContractGroup(GroupTable):
    """
    A Django model representing a part sold contract group.
    """
    contract_number = models.CharField(max_length=255)
    contract_date = models.DateTimeField()

    def manager(self, search_date, use_cache):
        return PartSoldContractManager(self.id, search_date, use_cache)

    def __str__(self):
        return f"PartSoldContractGroup {self.id}"

class PartSoldContract(DataTable):
    part_sold_contract_group = models.ForeignKey(PartSoldContractGroup, on_delete= models.CASCADE)
    description = models.TextField()

    @property
    def group(self):
        return self.part_sold_contract_group
    
    def __str__(self):
        return f"PartSoldContract {self.id}"


class PartSoldContractManager(GeneralManager):
    group_model = PartSoldContractGroup
    data_model = PartSoldContract
    data_extension_models = []
    
    def __init__(self, part_sold_contract_group_id, search_date=None, use_cache=True):
        super().__init__(part_sold_contract_group_id, search_date, use_cache)
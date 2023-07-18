from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager
from backend.models import SapNumber, PartGroup, CustomerPlant, ContractGroup, Currency, PartRecipientGroup

class PartSoldGroup(GroupTable):
    """
    A Django model representing a part sold group.
    """
    part_recipient = models.ForeignKey(PartRecipientGroup, on_delete= models.CASCADE)
    customer_part_number_sap = models.CharField(max_length=255)

    class Meta:
        unique_together = ('part_recipient', 'customer_part_number_sap')

    def manager(self, search_date, use_cache):
        return PartSoldManager(self.id, search_date, use_cache)

    def __str__(self):
        return f"PartSoldGroup {self.id}"
    
class PartSold(DataTable):
    sap_number = models.ForeignKey(SapNumber, on_delete= models.CASCADE)
    part_sold_group = models.ForeignKey(PartSoldGroup, on_delete= models.CASCADE)
    customer_part_number = models.CharField(max_length=255)
    part_group = models.ManyToManyField(PartGroup,blank=False) 
    customer_plant = models.ForeignKey(CustomerPlant, on_delete= models.CASCADE)
    contract_group = models.ForeignKey(ContractGroup, on_delete= models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete= models.CASCADE)
    description = models.TextField()
    validity_start_date = models.DateTimeField()
    validity_end_date = models.DateTimeField()
    cbd_date = models.DateTimeField()

    @property
    def group(self):
        return self.part_sold_group

class PartSoldManager(GeneralManager):
    """
    A manager class for handling PartSold-related operations, extending the GeneralManager.
    """
    group_model = PartSoldGroup
    data_model = PartSold
    data_extension_model_list = []

    def __init__(self, project_group_id, search_date=None, use_cache=True):
        """
        Initialize a ProjectManager instance.

        Args:
            project_group_id (int): The ID of the ProjectGroup instance.
            search_date (datetime.datetime, optional): The date used for filtering data. Defaults to None.
            use_cache (bool, optional): Whether to use the cache for data retrieval. Defaults to True.
        """
        super().__init__(group_id=project_group_id, search_date=search_date, use_cache=use_cache)
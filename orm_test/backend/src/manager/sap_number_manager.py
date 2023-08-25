from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager

class SapNumberGroup(GroupTable):
    sap_number = models.CharField(max_length=255, unique=True)

    @property
    def manager(self):
        return SapNumberManager
    
    def __str__(self):
        return f"SapNumber {self.sap_number}"

class SapNumber(DataTable):
    sap_number_group = models.ForeignKey(SapNumberGroup, on_delete= models.DO_NOTHING)
    description = models.TextField()
    alu_net_weight = models.FloatField()

    @property
    def group(self):
        return self.sap_number_group

    def __str__(self):
        return f"SapNumber {self.sap_number}"

class SapNumberManager(GeneralManager):
    group_model = SapNumberGroup
    data_model = SapNumber
    data_extension_model_list = []
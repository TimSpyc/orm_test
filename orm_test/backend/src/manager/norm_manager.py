from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class NormGroup(GroupTable):
    number = models.CharField(max_length=255)

    class meta:
        unique_together = ('number')

    def __str__(self):
        return f"NormGroup {self.number}"

    @property
    def manager(self):
        return NormManager
        

class Norm(DataTable):
    norm_type = models.ForeignKey('NormType', on_delete= models.DO_NOTHING)
    norm_group = models.ForeignKey(NormGroup, on_delete= models.DO_NOTHING)
    description = models.CharField(max_length=255)
    file_group = models.ForeignKey(
        'FileGroup', 
        on_delete= models.DO_NOTHING, 
        null=True
    )

    @property
    def group(self):
        return self.norm_group
    
    def __str__(self):
        return f"Norm {self.norm_group}-{self.description}"
    
class NormManager(GeneralManager):
    GroupTable = NormGroup
    DataTable = Norm
    DataExtensionTableList = []
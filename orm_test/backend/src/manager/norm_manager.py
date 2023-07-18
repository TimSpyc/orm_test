from django.db import models
from backend.models import GroupTable, DataTable, FileGroup, NormType
from backend.src.auxiliary.manager import GeneralManager

class NormGroup(GroupTable):
    number = models.CharField(max_length=255)

    class _meta:
        unique_together = ('number')

    def __str__(self):
        return f"NormGroup {self.number}"

    def manager(self, search_date, use_cache):
        return NormManager(self.id, search_date, use_cache)
        

class Norm(DataTable):
    norm_type = models.ForeignKey(NormType, on_delete= models.CASCADE)
    norm_group = models.ForeignKey(NormGroup, on_delete= models.CASCADE)
    description = models.CharField(max_length=255)
    file_group = models.ForeignKey(FileGroup, on_delete= models.CASCADE)

    @property
    def group(self):
        return self.norm_group
    
    def __str__(self):
        return f"Norm {self.norm_group}-{self.description}"
    
class NormManager(GeneralManager):
    GroupTable = NormGroup
    DataTable = Norm
    DataExtensionTableList = []

    def __init__(self, norm_group_id, search_date=None, use_cache=True):
        super().__init__(group_id=norm_group_id, search_date=search_date, use_cache=use_cache)
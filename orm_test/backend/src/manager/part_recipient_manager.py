from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager

class PartRecipientGroup(GroupTable):
    number = models.CharField(max_length=255, unique=True)

    @property
    def manager(self):
        return PartRecipientManager
    
    def __str__(self):
        return f"PartRecipientGroup {self.part_number}"

class PartRecipient(DataTable):
    part_recipient_group = models.ForeignKey(PartRecipientGroup, on_delete= models.DO_NOTHING)
    description = models.CharField(max_length=255)

    @property
    def group(self):
        return self.part_recipient_group
    
    def __str__(self):
        return f"PartRecipient {self.part_recipient_group}-{self.description}"
    
class PartRecipientManager(GeneralManager):
    group_model = PartRecipientGroup
    data_model = PartRecipient
    data_extension_model_list = []
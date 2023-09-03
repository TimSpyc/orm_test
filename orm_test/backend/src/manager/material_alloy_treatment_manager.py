from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class MaterialAlloyTreatmentGroup(GroupTable):
    temperature = models.FloatField()
    duration = models.FloatField()

    class meta:
        unique_together = ('temperature', 'duration')

    @property
    def manager(self):
        return MaterialAlloyTreatmentManager
    
    def __str__(self):
        return f"MaterialAlloyTreatmentGroup {self.id}"
    
class MaterialAlloyTreatment(DataTable):
    material_alloy_treatment_group = models.ForeignKey(MaterialAlloyTreatmentGroup, on_delete= models.DO_NOTHING)
    remark = models.TextField(default=None, null=True)
    
    @property
    def group_object(self):
        return self.material_alloy_treatment_group
    
    def __str__(self):
        return f"MaterialAlloyTreatment {self.material_alloy_treatment_group}-{self.description}"
    
class MaterialAlloyTreatmentManager(GeneralManager):
    group_model = MaterialAlloyTreatmentGroup
    data_model = MaterialAlloyTreatment
    data_extension_model_list = []
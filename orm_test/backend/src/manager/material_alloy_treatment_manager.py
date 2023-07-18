from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class MaterialAlloyTreatmentGroup(GroupTable):
    temperature = models.FloatField()
    duration = models.FloatField()

    class _meta:
        unique_together = ('temperature', 'duration')

    def manager(self, search_date, use_cache):
        return MaterialAlloyTreatmentManager(self.id, search_date, use_cache)
    
    def __str__(self):
        return f"MaterialAlloyTreatmentGroup {self.id}"
    
class MaterialAlloyTreatment(DataTable):
    material_alloy_treatment_group = models.ForeignKey(MaterialAlloyTreatmentGroup, on_delete= models.CASCADE)
    remark = models.TextField()
    
    @property
    def group(self):
        return self.material_alloy_treatment_group
    
    def __str__(self):
        return f"MaterialAlloyTreatment {self.material_alloy_treatment_group}-{self.description}"
    
class MaterialAlloyTreatmentManager(GeneralManager):
    group_model = MaterialAlloyTreatmentGroup
    data_model = MaterialAlloyTreatment
    data_extension_model_list = []

    def __init__(self, material_alloy_treatment_group_id, search_date=None, use_cache=True):
        super().__init__(group_id=material_alloy_treatment_group_id, search_date=search_date, use_cache=use_cache)
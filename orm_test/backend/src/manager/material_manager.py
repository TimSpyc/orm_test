from django.db import models
from backend.models import GroupTable, DataTable, MaterialAlloyGroup, MaterialAlloyTreatmentGroup, NormGroup, MaterialType
from backend.src.auxiliary.manager import GeneralManager

class MaterialGroup(GroupTable):

    def manager(self, search_date, use_cache):
        return MaterialManager(self.id, search_date, use_cache)
    
    def __str__(self):
        return f"MaterialGroup {self.id}"

class Material(DataTable):
    material_group = models.ForeignKey(MaterialGroup, on_delete= models.DO_NOTHING)
    material_type = models.ForeignKey(MaterialType, on_delete= models.DO_NOTHING)
    material_alloy = models.ForeignKey(MaterialAlloyGroup, on_delete= models.DO_NOTHING)
    material_alloy_treatment = models.ForeignKey(MaterialAlloyTreatmentGroup, on_delete= models.DO_NOTHING)
    customer_norm = models.ManyToManyField(NormGroup, blank=False)
    remark = models.TextField()
    extrusion_plant = models.ForeignKey(SupplierGroup, on_delete= models.DO_NOTHING)


    @property
    def group(self):
        return self.material_group
    
    def __str__(self):
        return f"Material {self.material_group}-{self.description}"

class MaterialManager(GeneralManager):
    group_model = MaterialGroup
    data_model = Material
    data_extension_model_list = []

    def __init__(self, material_group_id, search_date=None, use_cache=True):
        super().__init__(group_id=material_group_id, search_date=search_date, use_cache=use_cache)
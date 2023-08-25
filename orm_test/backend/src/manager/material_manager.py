from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class MaterialGroup(GroupTable):

    @property
    def manager(self):
        return MaterialManager
    
    def __str__(self):
        return f"MaterialGroup {self.id}"

class Material(DataTable):
    material_group = models.ForeignKey(MaterialGroup, on_delete= models.DO_NOTHING)
    material_type = models.ForeignKey('MaterialType', on_delete= models.DO_NOTHING)
    material_alloy = models.ForeignKey('MaterialAlloyGroup', on_delete= models.DO_NOTHING, null=True)
    material_alloy_treatment = models.ManyToManyField('MaterialAlloyTreatmentGroup', blank=True)
    customer_norm = models.ManyToManyField('NormGroup', blank=True)
    remark = models.TextField(null=True)
    rm_min = models.FloatField(null=True)
    rm_max = models.FloatField(null=True)
    rp_min = models.FloatField(null=True)
    rp_max = models.FloatField(null=True)
    a_min = models.FloatField(null=True)
    ag_min = models.FloatField(null=True)
    bending_angle_min = models.FloatField(null=True)
    #extrusion_plant = models.ForeignKey('SupplierGroup', on_delete= models.DO_NOTHING)

    @property
    def group(self):
        return self.material_group

    def __str__(self):
        return f"Material {self.material_group}-{self.description}"

class MaterialManager(GeneralManager):
    group_model = MaterialGroup
    data_model = Material
    data_extension_model_list = []
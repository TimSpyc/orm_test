from django.db import models
from backend.models import GroupTable, DataTable #NormGroup
from backend.src.auxiliary.manager import GeneralManager

class MaterialAlloyGroup(GroupTable):

    @property
    def manager(self):
        return MaterialAlloyManager
    
    def __str__(self):
        return f"MaterialAlloyGroup {self.number}"
    
class MaterialAlloy(DataTable):
    material_alloy_group = models.ForeignKey(MaterialAlloyGroup, on_delete= models.DO_NOTHING)
    norm = models.ForeignKey('NormGroup', on_delete= models.DO_NOTHING)
    chemical_symbol = models.CharField(max_length=255)
    internal_name = models.CharField(max_length=255, null=True)
    density = models.FloatField(null=True)
    silicon_min = models.FloatField(null=True)
    silicon_max = models.FloatField(null=True)
    iron_min = models.FloatField(null=True)
    iron_max = models.FloatField(null=True)
    copper_min = models.FloatField(null=True)
    copper_max = models.FloatField(null=True)
    manganese_min = models.FloatField(null=True)
    manganese_max = models.FloatField(null=True)
    magnesium_min = models.FloatField(null=True)
    magnesium_max = models.FloatField(null=True)
    chrome_min = models.FloatField(null=True)
    chrome_max = models.FloatField(null=True)
    zinc_min = models.FloatField(null=True)
    zinc_max = models.FloatField(null=True)
    titanium_min = models.FloatField(null=True)
    titanium_max = models.FloatField(null=True)
    lead_min = models.FloatField(null=True)
    lead_max = models.FloatField(null=True)
    tin_min = models.FloatField(null=True)
    tin_max = models.FloatField(null=True)
    vanadium_min = models.FloatField(null=True)
    vanadium_max = models.FloatField(null=True)
    cadmium_min = models.FloatField(null=True)
    cadmium_max = models.FloatField(null=True)
    nickel_min = models.FloatField(null=True)
    nickel_max = models.FloatField(null=True)
    phosphorus_min = models.FloatField(null=True)
    phosphorus_max = models.FloatField(null=True)
    sulfur_min = models.FloatField(null=True)
    sulfur_max = models.FloatField(null=True)
    carbon_min = models.FloatField(null=True)
    carbon_max = models.FloatField(null=True)
    permissible_additions = models.FloatField(null=True)
    
    @property
    def group(self):
        return self.material_alloy_group
    
    def __str__(self):
        return f"MaterialAlloy {self.material_alloy_group}-{self.description}"
    
class MaterialAlloyManager(GeneralManager):
    group_model = MaterialAlloyGroup
    data_model = MaterialAlloy
    data_extension_model_list = []

    def __init__(self, material_alloy_group_id, search_date=None, use_cache=True):
        super().__init__(group_id=material_alloy_group_id, search_date=search_date, use_cache=use_cache)
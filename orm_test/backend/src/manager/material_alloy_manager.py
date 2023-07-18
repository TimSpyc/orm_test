from django.db import models
from backend.models import GroupTable, DataTable, NormGroup
from backend.src.auxiliary.manager import GeneralManager

class MaterialAlloyGroup(GroupTable):

    def manager(self, search_date, use_cache):
        return MaterialAlloyManager(self.id, search_date, use_cache)
    
    def __str__(self):
        return f"MaterialAlloyGroup {self.number}"
    
class MaterialAlloy(DataTable):
    material_alloy_group = models.ForeignKey(MaterialAlloyGroup, on_delete= models.CASCADE)
    norm = models.ForeignKey(NormGroup, on_delete= models.CASCADE)
    chemical_symbol = models.CharField(max_length=255)
    density = models.FloatField()
    silicon_min = models.FloatField()
    silicon_max = models.FloatField()
    iron_min = models.FloatField()
    iron_max = models.FloatField()
    copper_min = models.FloatField()
    copper_max = models.FloatField()
    manganese_min = models.FloatField()
    manganese_max = models.FloatField()
    magnesium_min = models.FloatField()
    magnesium_max = models.FloatField()
    chrome_min = models.FloatField()
    chrome_max = models.FloatField()
    zinc_min = models.FloatField()
    zinc_max = models.FloatField()
    titanium_min = models.FloatField()
    titanium_max = models.FloatField()
    lead_min = models.FloatField()
    lead_max = models.FloatField()
    tin_min = models.FloatField()
    tin_max = models.FloatField()
    vanadium_min = models.FloatField()
    vanadium_max = models.FloatField()
    cadmium_min = models.FloatField()
    cadmium_max = models.FloatField()
    nickel_min = models.FloatField()
    nickel_max = models.FloatField()
    phosphorus_min = models.FloatField()
    phosphorus_max = models.FloatField()
    sulfur_min = models.FloatField()
    sulfur_max = models.FloatField()
    carbon_min = models.FloatField()
    carbon_max = models.FloatField()
    permissible_additions = models.FloatField()

    
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
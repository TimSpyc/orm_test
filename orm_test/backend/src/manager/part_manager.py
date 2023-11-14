from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class PartGroup(GroupTable):
    drawing_number = models.CharField(max_length=255)
    drawing_revision = models.IntegerField()

    class meta:
        constraints = [
            models.UniqueConstraint(
                fields=['drawing_no', 'drawing_rev'],
                name='unique_part_group'
            )
        ]

    @property
    def manager(self):
        return PartManager
    
    def __str__(self):
        return f"PartGroup {self.drawing_no}-{self.drawing_rev}"

class Part(DataTable):
    part_group = models.ForeignKey(PartGroup, on_delete= models.DO_NOTHING)
    name = models.CharField(max_length=255)
    part_type = models.ForeignKey('PartType', on_delete= models.DO_NOTHING)
    cross_section_group = models.ForeignKey('CrossSectionGroup', on_delete= models.DO_NOTHING)
    drawing_date = models.DateTimeField()
    customer_drawing_number = models.CharField(max_length=255)
    customer_drawing_revision = models.CharField(max_length=255)
    customer_part_number = models.CharField(max_length=255)
    customer_part_revision = models.CharField(max_length=255)
    surface_treatment = models.CharField(max_length=255)
    customer_surface_treatment = models.CharField(max_length=255)
    weight = models.FloatField()
    linear_weight = models.FloatField()
    length = models.FloatField()
    tolerance = models.CharField(max_length=255)
    customer_tolerance = models.CharField(max_length=255)
    semi_finished_product_type = models.ForeignKey('SemiFinishedProductType', on_delete= models.DO_NOTHING)
    material_group = models.ForeignKey('MaterialGroup', on_delete= models.DO_NOTHING)
    delivery_temper = models.CharField(max_length=255)
    material_norm_customer = models.ForeignKey('NormGroup', on_delete= models.DO_NOTHING)

    @property
    def group_object(self):
        return self.part_group

    def __str__(self):
        return f"Part {self.part_group}-{self.description}"

class PartManager(GeneralManager):
    group_model = PartGroup
    data_model = Part
    data_extension_model_list = []

from django.db import models
from backend.models import GroupTable, DataTable
from backend.src.auxiliary.manager import GeneralManager

class CrossSectionGroup(GroupTable):
    drawing_number = models.CharField(max_length=255)
    drawing_revision = models.IntegerField()

    class meta:
        unique_together = ('drawing_no', 'drawing_rev')

    def manager(self, search_date, use_cache):
        return CrossSectionManager(self.id, search_date, use_cache)
    
class CrossSection(DataTable):
    cross_section_group = models.ForeignKey('CrossSectionGroup', on_delete= models.DO_NOTHING)
    cross_section_tolerance_norm = models.ForeignKey('NormGroup', on_delete= models.DO_NOTHING)
    customer_tolerance = models.CharField(max_length=255)
    extrusion_plant_tooling_number = models.CharField(max_length=255)
    outer_contour_info_dict = models.JSONField(null=True, default=None)
    chambers_info_dict = models.JSONField(null=True, default=None)
    number_of_chambers = models.IntegerField(null=True, default=None)
    dimension_x = models.FloatField(null=True, default=None)
    dimension_y = models.FloatField(null=True, default=None)
    smallest_enclosing_circle_midpoint_x = models.FloatField(null=True, default=None)
    smallest_enclosing_circle_midpoint_y = models.FloatField(null=True, default=None)
    smallest_enclosing_circle_radius = models.FloatField(null=True, default=None)
    smallest_enclosing_circle_scope = models.FloatField(null=True, default=None)
    critical_radii_info_dict = models.JSONField(null=True, default=None)
    number_of_critical_radii = models.IntegerField(null=True, default=None)
    min_radius = models.FloatField(null=True, default=None)
    sharp_edge_info_dict = models.JSONField(null=True, default=None)
    number_of_sharp_edges = models.IntegerField(null=True, default=None)
    center_of_mass_x = models.FloatField(null=True, default=None)
    center_of_mass_y = models.FloatField(null=True, default=None)
    distance_to_center_of_mass_smallest_enclosing_circle = models.FloatField(null=True, default=None)
    flanges_info_dict = models.JSONField(null=True, default=None)
    number_of_flanges = models.IntegerField(null=True, default=None)
    max_flange_length = models.FloatField(null=True, default=None)
    number_of_critical_flanges = models.IntegerField(null=True, default=None)
    webs_info_dict = models.JSONField(null=True, default=None)
    number_of_critical_webs = models.IntegerField(null=True, default=None)
    nodes_info_dict = models.JSONField(null=True, default=None)
    number_of_nodes = models.IntegerField(null=True, default=None)
    number_of_critical_nodes = models.IntegerField(null=True, default=None)
    number_max_webs_on_node = models.IntegerField(null=True, default=None)
    number_critical_web_angles = models.IntegerField(null=True, default=None)
    min_web_angle = models.FloatField(null=True, default=None)
    surface_area = models.FloatField(null=True, default=None)
    area_ratio = models.FloatField(null=True, default=None)
    narrowest_point = models.FloatField(null=True, default=None)
    widest_point = models.FloatField(null=True, default=None)
    thickness_ratio = models.FloatField(null=True, default=None)
    evaluation_info_dict = models.JSONField(null=True, default=None)

    @property
    def group(self):
        return self.cross_section_group

    def __str__(self):
        return f"CrossSection {self.cross_section_group}-{self.description}"
    
class CrossSectionManager(GeneralManager):
    group_model = CrossSectionGroup
    data_model = CrossSection
    data_extension_model_list = []

    def __init__(self, sap_number_group_id, search_date=None, use_cache=True):
        super().__init__(group_id=sap_number_group_id, search_date=search_date, use_cache=use_cache)
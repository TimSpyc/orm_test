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
    cross_section_tolerance_norm = models.ForeignKey('NormGroup', on_delete= models.DO_NOTHING)
    customer_tolerance = models.CharField(max_length=255)
    extrusion_plant_tooling_number = models.CharField(max_length=255)
    outer_contour_info_dict = models.JSONField()
    chambers_info_dict = models.JSONField()
    number_of_chambers = models.IntegerField()
    dimension_x = models.FloatField()
    dimension_y = models.FloatField()
    smallest_enclosing_circle_midpoint_x = models.FloatField()
    smallest_enclosing_circle_midpoint_y = models.FloatField()
    smallest_enclosing_circle_radius = models.FloatField()
    smallest_enclosing_circle_scope = models.FloatField()
    critical_radii_info_dict = models.JSONField()
    number_of_critical_radii = models.IntegerField()
    min_radius = models.FloatField()
    sharp_edge_info_dict = models.JSONField()
    number_of_sharp_edges = models.IntegerField()
    center_of_mass_x = models.FloatField()
    center_of_mass_y = models.FloatField()
    distance_to_center_of_mass_smallest_enclosing_circle = models.FloatField()
    flanges_info_dict = models.JSONField()
    number_of_flanges = models.IntegerField()
    max_flange_length = models.FloatField()
    number_of_critical_flanges = models.IntegerField()
    webs_info_dict = models.JSONField()
    number_of_critical_webs = models.IntegerField()
    nodes_info_dict = models.JSONField()
    number_of_nodes = models.IntegerField()
    number_of_critical_nodes = models.IntegerField()
    number_max_webs_on_node = models.IntegerField()
    number_critical_web_angles = models.IntegerField()
    min_web_angle = models.FloatField()
    surface_area = models.FloatField()
    area_ratio = models.FloatField()
    narrowest_point = models.FloatField()
    widest_point = models.FloatField()
    thickness_ratio = models.FloatField()
    evaluation_info_dict = models.JSONField()

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
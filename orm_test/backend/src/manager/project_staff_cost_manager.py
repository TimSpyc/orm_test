from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager
from datetime import datetime

class ProjectStaffCostGroup(GroupTable):
    project_group = models.ForeignKey("ProjectGroup", on_delete=models.DO_NOTHING)
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING)
    project_staff_cost_task = models.ForeignKey("ProjectStaffCostTask", on_delete=models.DO_NOTHING)
    work_date = models.DateField()

    class Meta:
       unique_together = ('project_group','user','project_staff_cost_task','work_date')

    def __str__(self):
        return f'Project_staff_cost_group {self.id}'
    
    def manager(self, search_date, use_cache):
        return ProjectStaffCostManager(self.id, search_date, use_cache)

class ProjectStaffCost(DataTable): 
    project_staff_cost_group = models.ForeignKey(ProjectStaffCostGroup, on_delete=models.DO_NOTHING)
    hours = models.FloatField()

    def __str__(self):
        return f'Project_staff_cost {self.id}'
    
    @property
    def group(self):
        return self.project_staff_cost_group

class ProjectStaffCostManager(GeneralManager):
    group_model = ProjectStaffCostGroup
    data_model = ProjectStaffCost
    data_extension_models = []

    def __init__(self, project_staff_cost_group_id, search_date, use_cache):
        super().__init__(project_staff_cost_group_id, search_date, use_cache)
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

    @property
    def manager(self):
        return ProjectStaffCostManager

class ProjectStaffCost(DataTable): 
    project_staff_cost_group = models.ForeignKey(ProjectStaffCostGroup, on_delete=models.DO_NOTHING)
    hours = models.FloatField()

    def __str__(self):
        return f'Project_staff_cost {self.id}'
    
    @property
    def group_object(self):
        return self.project_staff_cost_group

class ProjectStaffCostManager(GeneralManager):
    group_model = ProjectStaffCostGroup
    data_model = ProjectStaffCost
    data_extension_models = []
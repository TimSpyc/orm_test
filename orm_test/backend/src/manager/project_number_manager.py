from django.db import models
from backend.models import GroupTable, DataTable, ExternalDataTable
from backend.src.auxiliary.manager import GeneralManager, ExternalDataManager
from backend.models.validators.regex_validators import RegexValidator

class ProjectNumberGroup(GroupTable):
    """
    A Django model representing a project number group.
    """
    project_number = models.CharField(max_length=255, unique=True)

    validator_list = [
        RegexValidator("project_number", r"AP\d{5}"),
    ]

    def __str__(self):
        return f'Project_number_group {self.id}'

    @property
    def manager(self):
        return ProjectNumberManager

class ProjectNumber(DataTable):
    """
    A Django model representing a project number, including its network number
    and associated project number group.
    """ 
    project_number_group = \
        models.ForeignKey(ProjectNumberGroup, on_delete=models.DO_NOTHING)
    network_number = models.BigIntegerField(null=True)

    def __str__(self):
        return f'project_number {self.id}'
    
    @property
    def group_object(self):
        return self.project_number_group

class ProjectNumberManager(GeneralManager):
    """
    A manager class for handling ProjectNumber-related operations, extending 
    the GeneralManager.

    Attributes:
        group_model (models.Model): The ProjectNumberGroup model.
        data_model (models.Model): The ProjectNumber model.
    """
    group_model = ProjectNumberGroup
    data_model = ProjectNumber
    data_extension_model_list = []


class ProjectNumberFinancialOverview(ExternalDataTable):
    project_number_group = models.ForeignKey(ProjectNumberGroup, on_delete=models.DO_NOTHING)
    psp_cat_1 = models.CharField(max_length=2, null=False)
    psp_cat_2 = models.CharField(max_length=2, null=False)
    costs = models.DecimalField(decimal_places=2, max_digits=20, null=False)
    booking_date = models.DateField(null=False)


class ProjectNumberFinancialOverviewManager(ExternalDataManager):
    database_model = ProjectNumberFinancialOverview

    def __init__(self, project_number_group_id):
        self.project_number_group_id = project_number_group_id
        self.project_number_financial_overview_list_of_dict = \
            self.getProjectNumberFinancialOverviewListOfDict()


    def getProjectNumberFinancialOverviewListOfDict(self):
        result = self.getData(
            column_list = ['psp_cat_1', 'psp_cat_2', 'costs', 'booking_date'],
            project_number_group_id = self.project_number_group_id
        )

        return result


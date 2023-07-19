from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .abstract_models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from .reference_models import User
from backend.src.manager.project_manager import ProjectGroup

class ProjectUserGroup(GroupTable):
    """
    A Django model representing a project user group, which associates a
    user with a project group.
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('user', 'project_group')

    def __str__(self):
        return f"{self.user} - {self.project_group}"


class ProjectUserRole(ReferenceTable):
    """
    A Django model representing a project user role, which includes a role
    name.
    """
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name

class DerivativeType(ReferenceTable):
    """
    A Django model representing a derivative type, which includes a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProjectUser(DataTable):
    """
    A Django model representing a project user, including their project user
    group and project user roles.
    """
    project_user_group = models.ForeignKey(
        ProjectUserGroup,
        on_delete=models.DO_NOTHING
    )
    project_user_role = models.ManyToManyField(ProjectUserRole, blank=False)

    def __str__(self):
        return f'ProjectUser {self.id}'


class DerivativeConstelliumGroup(GroupTable):
    """
    A Django model representing a derivative Constellium group, which
    associates a derivative Constellium group with a project group.
    """
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}"


class PredictionAccuracy(ReferenceTable):
    """
    A Django model representing a prediction accuracy, which includes a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DerivativeConstellium(DataTable):
    """
    A Django model representing a derivative Constellium, including its name,
    start and end dates, derivative type, estimated price, estimated weight,
    and prediction accuracy.
    """
    derivative_constellium_group = models.ForeignKey(
        DerivativeConstelliumGroup,
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=255)
    sop_date = models.DateField()
    eop_date = models.DateField()
    derivative_type = models.ForeignKey(
        DerivativeType,
        on_delete=models.DO_NOTHING
    )
    estimated_price = models.FloatField()
    estimated_weight = models.FloatField()
    prediction_accuracy = models.ForeignKey(
        PredictionAccuracy,
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.name

class Customer(ReferenceTable):
    company_name = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.company_name} ({self.group_name})"

class CustomerPlant(ReferenceTable):
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name} - {self.customer}"

class RevisionLMC(ReferenceTable):
    revision_date = models.DateField()

    def __str__(self):
        return self.revision_date.strftime('%Y-%m')

class DerivativeLMCGroup(GroupTable):
    lmc_full_code = models.CharField(max_length=255, unique=True)
    lmc_model_code = models.CharField(max_length=255)

    class Meta:
        unique_together = ('lmc_full_code', 'lmc_model_code')

    def __str__(self):
        return f"{self.lmc_full_code} - {self.lmc_model_code}"

class DerivativeLMC(DataTable):
    derivative_lmc_group = models.ForeignKey(DerivativeLMCGroup, on_delete=models.DO_NOTHING)
    revision_lmc = models.ForeignKey(RevisionLMC, on_delete=models.DO_NOTHING)
    region = models.CharField(max_length=255)
    trade_region = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    sales_group = models.ForeignKey(Customer, related_name='sales_groups', on_delete=models.DO_NOTHING)
    manufacturer = models.ForeignKey(Customer, related_name='manufacturers', on_delete=models.DO_NOTHING)
    local_make = models.ForeignKey(Customer, related_name='local_makes', on_delete=models.DO_NOTHING)
    local_model_line = models.CharField(max_length=255)
    local_program_code = models.CharField(max_length=255)
    local_production_model = models.CharField(max_length=255)
    global_make = models.ForeignKey(Customer, related_name='global_makes', on_delete=models.DO_NOTHING)
    global_production_model = models.CharField(max_length=255)
    gvw = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    plant = models.ForeignKey(CustomerPlant, on_delete=models.DO_NOTHING)
    production_type = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=255, db_column='type')
    regional_size = models.CharField(max_length=255)
    regional_body_type = models.CharField(max_length=255)
    regional_status = models.CharField(max_length=255)
    global_size = models.CharField(max_length=255)
    global_body_type = models.CharField(max_length=255)
    global_status = models.CharField(max_length=255)
    sop_date = models.DateField()
    eop_date = models.DateField()
    next_facelift = models.DateField()
    last_actual = models.DateField()
    design_lead = models.ForeignKey(Customer, related_name='design_leads', on_delete=models.DO_NOTHING)
    design_lead_location = models.CharField(max_length=255)
    design_lead_country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.derivative_group_lmc} - {self.local_make} {self.local_model_line}"

class DerivativeVolumeLMCGroup(GroupTable):
    derivative_lmc_group = models.ForeignKey(DerivativeLMCGroup, on_delete=models.DO_NOTHING, null=False)
    date = models.DateField(null=False)

    class Meta:
        unique_together = ('derivative_lmc_group', 'date')

    def __str__(self):
        return f"Derivative Volume Group {self.id}: {self.derivative_group.lmc_full_code} - {self.date}"

class DerivativeVolumeLMC(DataTable):
    derivative_lmc_volume_group = models.ForeignKey(DerivativeVolumeLMCGroup, on_delete=models.DO_NOTHING)
    revision_lmc = models.ForeignKey(RevisionLMC, on_delete=models.DO_NOTHING)
    volume = models.PositiveIntegerField()

    def __str__(self):
        return f"LMC Derivative Volume {self.id}: {self.volume_group.derivative_group.lmc_full_code} - {self.revision_lmc.revision_date} - {self.volume}"


class DerivativeVolumeLMCDerivativeConstelliumConnectionGroup(GroupTable):
    derivative_lmc_group = models.ForeignKey(DerivativeLMCGroup, on_delete=models.DO_NOTHING)
    derivative_constellium_group = models.ForeignKey(DerivativeConstelliumGroup, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('derivative_lmc_group', 'derivative_constellium_group')

    def __str__(self):
        return f"Derivative Volume Group {self.id}: {self.derivative_lmc_group.lmc_full_code} - {self.derivative_constellium_group.id}"


class DerivativeVolumeLMCDerivativeConstelliumConnection(DataTable):
    derivative_volume_lmc_derivative_constellium_connection_group = models.ForeignKey(DerivativeVolumeLMCDerivativeConstelliumConnectionGroup, on_delete=models.DO_NOTHING)
    take_rate = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        group = self.derivative_volume_lmc_derivative_constellium_connection_group
        return f"LMC Derivative Volume connection: {group.derivative_lmc_group.lmc_full_code} - {group.derivative_constellium_group.id} - take_rate: {self.take_rate}"


# #Dummy for PartGroup
# class PartGroup(GroupTable):
#     pass
# #Dummy for FileGroup
# class FileGroup(GroupTable):
#     pass

# class ChangeRequestGroup(GroupTable):
#     project_group = models.ForeignKey(ProjectGroup, on_delete=models.DO_NOTHING)
#     change_request_no = models.IntegerField()

#     class Meta:
#         unique_together = ('project_group', 'change_request_no')

#     def __str__(self):
#         return f"ChangeRequestGroup {self.id}"


# class ChangeRequest(DataTable):
#     change_request_group = models.ForeignKey(ChangeRequestGroup, on_delete=models.DO_NOTHING)
#     derivative_constellium_group = models.ForeignKey(DerivativeConstelliumGroup, on_delete=models.DO_NOTHING)
#     customer_part_number = models.CharField(max_length=255)
#     description = models.TextField()
#     ECR_number = models.CharField(max_length=255)
#     customer_approval = models.BooleanField(default=False)
#     internal_approval = models.BooleanField(default=False)
#     part_group_before_change = models.ForeignKey(PartGroup, on_delete=models.DO_NOTHING)
#     file_before_change = models.ForeignKey(FileGroup, on_delete=models.DO_NOTHING)
#     part_group_after_change = models.ForeignKey(PartGroup, on_delete=models.DO_NOTHING)
#     file_after_change = models.ForeignKey(FileGroup, on_delete=models.DO_NOTHING)
#     file_for_description = models.ForeignKey(FileGroup, on_delete=models.DO_NOTHING)


# class ChangeRequestFeasibilityGroup(GroupTable):
#     change_request_group = models.ForeignKey(ChangeRequestGroup, on_delete=models.DO_NOTHING)
#     project_user_role = models.ForeignKey(ProjectUserRole, on_delete=models.DO_NOTHING)

#     class Meta:
#         unique_together = ('project_user_role', 'change_request_group')

#     def __str__(self):
#         return f"ChangeRequestFeasibilityGroup {self.id}: {self.change_request_group.id}; {self.project_user_role.role_name}"


# class ChangeRequestFeasibility(DataTable):
#     change_request_feasibility_group = models.ForeignKey(ChangeRequestFeasibilityGroup, on_delete=models.DO_NOTHING)
#     confirmed = models.BooleanField(null=True)
#     description = models.TextField()


# class ChangeRequestCostGroup(GroupTable):
#     change_request_group = models.ForeignKey(ChangeRequestGroup, on_delete=models.DO_NOTHING)
#     project_user_role = models.ForeignKey(ProjectUserRole, on_delete=models.DO_NOTHING)

#     class Meta:
#         unique_together = ('change_request_group', 'project_user_role')

#     def __str__(self):
#         return f"ChangeRequestCostGroup {self.id}: {self.change_request_group.id}; {self.project_user_role.role_name}"


# class ChangeRequestCost(DataTable):
#     change_request_cost_group = models.ForeignKey(ChangeRequestCostGroup, on_delete=models.DO_NOTHING)
#     description = models.TextField(null=True)
#     cost_estimation = models.IntegerField(null=True)


# class ChangeRequestRiskGroup(GroupTable):
#     change_request_group = models.ForeignKey(ChangeRequestGroup, on_delete=models.DO_NOTHING)
#     project_user_role = models.ForeignKey(ProjectUserRole, on_delete=models.DO_NOTHING)

#     def __str__(self):
#         return f"ChangeRequestRiskGroup {self.id}: {self.change_request_group.id}; {self.user.first_name} {self.user.last_name}"


# class ChangeRequestRiskProbability(ReferenceTable):
#     name = models.CharField(max_length=255)
#     factor = models.IntegerField()


# class ChangeRequestRiskImpact(ReferenceTable):
#     name = models.CharField(max_length=255)
#     factor = models.IntegerField()


# class ChangeRequestRisk(DataTable):
#     change_request_risk_group = models.ForeignKey(ChangeRequestRiskGroup, on_delete=models.DO_NOTHING)
#     change_request_risk_probability = models.ForeignKey(ChangeRequestRiskProbability, on_delete=models.DO_NOTHING)
#     change_request_risk_impact = models.ForeignKey(ChangeRequestRiskImpact, on_delete=models.DO_NOTHING)
#     description = models.TextField()
#     feedback = models.TextField()
#     next_step = models.TextField()


class ProjectStaffCostTask(ReferenceTable):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProjectStaffCostGroup(GroupTable):
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project_staff_cost_task = models.ForeignKey(ProjectStaffCostTask, on_delete=models.DO_NOTHING)
    work_date = models.BigIntegerField()

    class Meta:
       unique_together = ('project_group','user','project_staff_cost_task','work_date')

    def __str__(self):
        return f'Project_staff_cost_group {self.id}'
    

class ProjectStaffCost(DataTable): 
    project_staff_cost_group = models.ForeignKey(ProjectStaffCostGroup, on_delete=models.DO_NOTHING)
    hours = models.FloatField()

    def __str__(self):
        return f'Project_staff_cost {self.id}'


class ScenarioGroup(GroupTable):
    """
    A Django model representing a scenario group.
    """
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.id


class Scenario(DataTable):
    """
    A Django model representing a scenario, including its name, data, and associated scenario group.
    """
    name = models.CharField(max_length=255)
    data = models.JSONField()

    def __str__(self):
        return self.name

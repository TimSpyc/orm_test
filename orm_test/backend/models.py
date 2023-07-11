from django.db import models
from django.db.models import Max, Subquery, Q
from django.core.validators import MinValueValidator, MaxValueValidator
import pickle, json
from datetime import datetime
from datetime import datetime

class GroupTable(models.Model):
    """
    An abstract Django model for representing group tables.
    """
    class Meta:
        abstract = True

class ReferenceTable(models.Model):
    """
    An abstract Django model for representing reference tables.
    """
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class User(ReferenceTable):
    """
    A Django model representing a User with a Microsoft ID, name, last name,
    email, and last login date.
    """
    microsoft_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class DataTable(models.Model):
    """
    An abstract Django model for representing data tables, including date,
    creator, and active status.
    """
    date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class CacheManager(models.Model):
    """
    A Django model representing cache entries, which store the manager name,
    group ID, date, and pickled data.
    """
    manager_name = models.CharField(max_length=100)
    group_id = models.IntegerField()
    date = models.DateTimeField()
    data = models.BinaryField()

    class Meta:
        unique_together = ('manager_name', 'group_id', 'date')

    @classmethod
    def get_cache_data(
        cls,
        manager_name: str,
        group_model_obj: models.Model,
        group_model_name: str,
        data_model: models.Model,
        input_group_id: int,
        date: datetime | None
    ) -> object | None:
        """
        Retrieve cached data for a given manager name, group model object,
        group model name, data model, input group ID, and date.
        
        Args:
            manager_name (str): The name of the manager.
            group_model_obj (models.Model): The group model object.
            group_model_name (str): The name of the group model.
            data_model (models.Model): The data model.
            input_group_id (int): The input group ID.
            date (datetime.datetime): The date used for filtering the cached
                data. If set to None, the latest date will be used.

        Returns:
            object: The cached data as a Python object, or None if no cache
            entry is found.
        """
        try:
            if date is None:
                latest_dates = data_model.objects.filter(
                    **{group_model_name: group_model_obj}
                ).values(group_model_name).annotate(latest_date=Max('date'))
            else:
                latest_dates = data_model.objects.filter(
                    **{'date__lt': date, group_model_name:group_model_obj}
                ).values(group_model_name).annotate(latest_date=Max('date'))

            result = cls.objects.filter(
                manager_name=manager_name,
                date=latest_dates.values('latest_date')[:1],
                group_id=input_group_id
            )
            if result.exists():
                entry = result.first()
                return pickle.loads(entry.data)
        except cls.DoesNotExist:
            pass
        except data_model.DoesNotExist:
            raise ValueError(f'data_model {data_model} is not valid')
        return None

    @classmethod
    def set_cache_data(
        cls,
        manager_name: str,
        group_id: int,
        data: object,
        date: datetime
    ) -> None:
        """
        Store data in the cache for a given manager name, group ID, data, and
        date.

        Args:
            manager_name (str): The name of the manager.
            group_id (int): The group ID.
            data (object): The data to be stored in the cache as a Python
                object.
            date (datetime.datetime): The date for the cache entry.

        Returns:
            None
        """
        entry, _ = cls.objects.get_or_create(
            manager_name=manager_name,
            group_id=group_id,
            date=date
        )
        entry.data=pickle.dumps(data)
        entry.save()


class CacheIntermediate(models.Model):
    """
    A Django model representing cache entries, which store the
    intermediate name, identification, start_date, end_date and pickled data.
    """
    intermediate_name = models.CharField(max_length=100)
    identification = models.JSONField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    data = models.BinaryField()

    class Meta:
        unique_together = (
            'intermediate_name',
            'identification',
            'start_date',
            'end_date'
        )

    @classmethod
    def get_cache_data(
        cls,
        intermediate_name: str,
        identification_dict: dict,
        date: datetime | None
    ) -> object | None:
        """
        Get cached data based on intermediate_name, identification_dict, and
        date. If date is None, use the current datetime.

        Args:
            intermediate_name (str): The intermediate name.
            identification_dict (dict): The identification dictionary.
            date (datetime | None): The datetime to filter the data.

        Returns:
            object: The cached data if found, None otherwise.
        """
        if date is None:
            date = datetime.now()
        try:
            result = cls.objects.filter(
                Q(start_date__lte=date, end_date__gte=date) | 
                Q(start_date__lte=date, end_date__isnull=True),
                intermediate_name=intermediate_name,
                identification = cls.getIdString(identification_dict),
            )
            if result.exists():
                entry = result.first()
                return pickle.loads(entry.data)
        except cls.DoesNotExist:
            pass
        return None

    @classmethod
    def set_cache_data(
        cls,
        intermediate_name: str,
        identification_dict: dict,
        data: object,
        start_date: datetime,
        end_date: datetime | None
    ) -> None:
        """
        Set cached data based on intermediate_name, identification_dict,
        start_date, end_date and data.

        Args:
            intermediate_name (str): The intermediate name.
            identification_dict (dict): The identification dictionary.
            data (object): The data to be cached.
            start_date (datetime): The start datetime of the cache data.
            end_date (datetime | None): The end datetime of the cache data.
        """
        entry, _ = cls.objects.get_or_create(
            intermediate_name=intermediate_name,
            identification=cls.getIdString(identification_dict),
            start_date=start_date,
            end_date=end_date
        )
        entry.data=pickle.dumps(data)
        entry.save()

    @staticmethod
    def getIdString(identification_dict: dict) -> str:
        """
        Convert an identification_dict into a JSON string, with keys sorted.

        Args:
            identification_dict (dict): The identification dictionary.

        Returns:
            str: The sorted JSON string of the identification dictionary.
        """
        return json.dumps(identification_dict, sort_keys=True)


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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.customer}"


class Currency(ReferenceTable):
    """
    A Django model representing the currencies euro, us-dollar, yuan
    and swiss franks
    """
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class ProjectStatus(ReferenceTable):
    """
    A Django model representing the project status which includes a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProjectType(ReferenceTable):
    """
    A Django model representing the project type which includes a name.
    """
    name = models.CharField(max_length=255)  

    def __str__(self):
        return self.name
    
class ProjectNumber(ReferenceTable):
    """
    A Django model representing the project number .
    """
    project_number = models.CharField(max_length=255)  

    def __str__(self):
        return self.project_number
   
class FileExtension(ReferenceTable):
    """
    A Django model representing the file extension which includes a name.
    """
    name = models.CharField(max_length=255)  
    
class FileType(ReferenceTable):
    """
    A Django model representing the file type which includes a name 
    and file extension
    """
    name = models.CharField(max_length=255)  
    file_extension = models.ManyToManyField(FileExtension)

    def __str__(self):
        return self.name     

class FileGroup(GroupTable):
    """
    A Django model representing a file group.
    """
    name = models.CharField(max_length=255)  

    def __str__(self):
        return self.name
    
class File(DataTable):
    """
    A Django model representing a project group.
    """
    file_type = models.ForeignKey(FileType, on_delete=models.CASCADE)
    data = models.BinaryField()
    file_group = models.ForeignKey(FileGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class ProjectGroup(GroupTable):
    """
    A Django model representing a project group.
    """
    def __str__(self):
        return self.id

class Project(DataTable):
    """
    A Django model representing a project, including its name, project number, 
    project_status, project_type, currency, file, customer, probability_of_nomination
    and associated project group and user.
    """
    name = models.CharField(max_length=255)
    project_number = models.ForeignKey(ProjectNumber, on_delete=models.CASCADE)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)
    project_status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE)
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    file_group = models.ForeignKey(FileGroup, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    probability_of_nomination = models.FloatField(null=True)

    # class Meta:
    #     unique_together = ('project_number', 'project_group')

    def __str__(self):
        return self.name

class ProjectUserGroup(GroupTable):
    """
    A Django model representing a project user group, which associates a
    user with a project group.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project_group')

    def __str__(self):
        return f"{self.user} - {self.project_group}"

class ProjectUserRole(ReferenceTable):
    """
    A Django model representing a project user role, which includes a role
    name.
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
        on_delete=models.CASCADE
    )
    project_user_role = models.ManyToManyField(ProjectUserRole, blank=False)

    def __str__(self):
        return f'ProjectUser {self.id}'


class DerivativeConstelliumGroup(GroupTable):
    """
    A Django model representing a derivative Constellium group, which
    associates a derivative Constellium group with a project group.
    """
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class DerivativeType(ReferenceTable):
    """
    A Django model representing a derivative type, which includes a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PredictionAccuracy(ReferenceTable):
    """
    A Django model representing a prediction accuracy, which includes a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Location(ReferenceTable):
    name = models.CharField(max_length=255)
    
class DerivativeConstellium(DataTable):
    """
    A Django model representing a derivative Constellium, including its name,
    start and end dates, derivative type, estimated price, estimated weight,
    and prediction accuracy.
    """
    derivative_constellium_group = models.ForeignKey(
        DerivativeConstelliumGroup,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    sop_date = models.DateField()
    eop_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    derivative_type = models.ForeignKey(
        DerivativeType,
        on_delete=models.CASCADE
    )
    estimated_price = models.FloatField()
    estimated_weight = models.FloatField()
    prediction_accuracy = models.ForeignKey(
        PredictionAccuracy,
        on_delete=models.CASCADE
    )
    file_group = models.ForeignKey(FileGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
    derivative_lmc_group = models.ForeignKey(DerivativeLMCGroup, on_delete=models.CASCADE)
    revision_lmc = models.ForeignKey(RevisionLMC, on_delete=models.CASCADE)
    region = models.CharField(max_length=255)
    trade_region = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    sales_group = models.ForeignKey(Customer, related_name='sales_groups', on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Customer, related_name='manufacturers', on_delete=models.CASCADE)
    local_make = models.ForeignKey(Customer, related_name='local_makes', on_delete=models.CASCADE)
    local_model_line = models.CharField(max_length=255)
    local_program_code = models.CharField(max_length=255)
    local_production_model = models.CharField(max_length=255)
    global_make = models.ForeignKey(Customer, related_name='global_makes', on_delete=models.CASCADE)
    global_production_model = models.CharField(max_length=255)
    gvw = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    plant = models.ForeignKey(CustomerPlant, on_delete=models.CASCADE)
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
    design_lead = models.ForeignKey(Customer, related_name='design_leads', on_delete=models.CASCADE)
    design_lead_location = models.CharField(max_length=255)
    design_lead_country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.derivative_group_lmc} - {self.local_make} {self.local_model_line}"

class DerivativeVolumeLMCGroup(GroupTable):
    derivative_lmc_group = models.ForeignKey(DerivativeLMCGroup, on_delete=models.CASCADE, null=False)
    date = models.DateField(null=False)

    class Meta:
        unique_together = ('derivative_lmc_group', 'date')

    def __str__(self):
        return f"Derivative Volume Group {self.id}: {self.derivative_group.lmc_full_code} - {self.date}"

class DerivativeVolumeLMC(DataTable):
    derivative_lmc_volume_group = models.ForeignKey(DerivativeVolumeLMCGroup, on_delete=models.CASCADE)
    revision_lmc = models.ForeignKey(RevisionLMC, on_delete=models.CASCADE)
    volume = models.PositiveIntegerField()

    def __str__(self):
        return f"LMC Derivative Volume {self.id}: {self.volume_group.derivative_group.lmc_full_code} - {self.revision_lmc.revision_date} - {self.volume}"


class DerivativeVolumeLMCDerivativeConstelliumConnectionGroup(GroupTable):
    derivative_lmc_group = models.ForeignKey(DerivativeLMCGroup, on_delete=models.CASCADE)
    derivative_constellium_group = models.ForeignKey(DerivativeConstelliumGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('derivative_lmc_group', 'derivative_constellium_group')

    def __str__(self):
        return f"Derivative Volume Group {self.id}: {self.derivative_lmc_group.lmc_full_code} - {self.derivative_constellium_group.id}"


class DerivativeVolumeLMCDerivativeConstelliumConnection(DataTable):
    derivative_volume_lmc_derivative_constellium_connection_group = models.ForeignKey(DerivativeVolumeLMCDerivativeConstelliumConnectionGroup, on_delete=models.CASCADE)
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

class ChangeRequestGroup(GroupTable):
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)
    change_request_no = models.IntegerField()

    class Meta:
        unique_together = ('project_group', 'change_request_no')

    def __str__(self):
        return f"ChangeRequestGroup {self.id}"


class ChangeRequest(DataTable):
    change_request_group = models.ForeignKey(ChangeRequestGroup, on_delete=models.CASCADE)
    derivative_constellium_group = models.ForeignKey(DerivativeConstelliumGroup, on_delete=models.CASCADE)
    customer_part_number = models.CharField(max_length=255)
    customer_part_name = models.CharField(max_length=255)
    description = models.TextField()
    ECR_number = models.CharField(max_length=255)
    customer_approval = models.BooleanField(default=False)
    internal_approval = models.BooleanField(default=False)
    #part_group_before_change = models.ForeignKey(PartGroup, on_delete=models.CASCADE)
    # file_group_before_change = models.ForeignKey(FileGroup, on_delete=models.CASCADE, related_name='file_group_before_change')
    # part_group_after_change = models.ForeignKey(PartGroup, on_delete=models.CASCADE)
    # file_group_after_change = models.ForeignKey(FileGroup, on_delete=models.CASCADE,related_name='file_group_after_change')
    # file_for_description = models.ForeignKey(FileGroup, on_delete=models.CASCADE, related_name='file_for_description')


class ChangeRequestFeasibilityGroup(GroupTable):
    change_request_group = models.ForeignKey(ChangeRequestGroup, on_delete=models.CASCADE)
    project_user_role = models.ForeignKey(ProjectUserRole, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project_user_role', 'change_request_group')

    def __str__(self):
        return f"ChangeRequestFeasibilityGroup {self.id}: {self.change_request_group.id}; {self.project_user_role.role_name}"


class ChangeRequestFeasibility(DataTable):
    change_request_feasibility_group = models.ForeignKey(ChangeRequestFeasibilityGroup, on_delete=models.CASCADE)
    confirmed = models.BooleanField(null=True)
    description = models.TextField()
    
class ChangeRequestFile(DataTable):
    change_request_group = models.ForeignKey(ChangeRequestGroup, on_delete=models.CASCADE)
    file_group = models.ForeignKey(FileGroup, on_delete=models.CASCADE)
    description = models.TextField()


class ChangeRequestCostGroup(GroupTable):
    change_request_group = models.ForeignKey(ChangeRequestGroup, on_delete=models.CASCADE)
    project_user_role = models.ForeignKey(ProjectUserRole, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('change_request_group', 'project_user_role')

    def __str__(self):
        return f"ChangeRequestCostGroup {self.id}: {self.change_request_group.id}; {self.project_user_role.role_name}"


class ChangeRequestCost(DataTable):
    change_request_cost_group = models.ForeignKey(ChangeRequestCostGroup, on_delete=models.CASCADE)
    description = models.TextField(null=True)  ##null =true richtig so ?
    cost_estimation = models.IntegerField(null=True)


class ChangeRequestRiskGroup(GroupTable):
    change_request_group = models.ForeignKey(ChangeRequestGroup, on_delete=models.CASCADE)
    project_user_role = models.ForeignKey(ProjectUserRole, on_delete=models.CASCADE)

    def __str__(self):
        return f"ChangeRequestRiskGroup {self.id}: {self.change_request_group.id}; {self.user.first_name} {self.user.last_name}"


class ChangeRequestRiskProbability(ReferenceTable):
    name = models.CharField(max_length=255)
    factor = models.IntegerField()


class ChangeRequestRiskImpact(ReferenceTable):
    name = models.CharField(max_length=255)
    factor = models.IntegerField()


class ChangeRequestRisk(DataTable):
    change_request_risk_group = models.ForeignKey(ChangeRequestRiskGroup, on_delete=models.CASCADE)
    change_request_risk_probability = models.ForeignKey(ChangeRequestRiskProbability, on_delete=models.CASCADE)
    change_request_risk_impact = models.ForeignKey(ChangeRequestRiskImpact, on_delete=models.CASCADE)
    description = models.TextField()
    feedback = models.TextField()
    next_step = models.TextField()


class ProjectStaffCostTask(ReferenceTable):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProjectStaffCostGroup(GroupTable):
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_staff_cost_task = models.ForeignKey(ProjectStaffCostTask, on_delete=models.CASCADE)
    work_date = models.DateTimeField()

    class Meta:
       unique_together = ('project_group','user','project_staff_cost_task','work_date')

    def __str__(self):
        return f'Project_staff_cost_group {self.id}'
    

class ProjectStaffCost(DataTable): 
    project_staff_cost_group = models.ForeignKey(ProjectStaffCostGroup, on_delete=models.CASCADE)
    hours = models.FloatField()

    def __str__(self):
        return f'Project_staff_cost {self.id}'


class ScenarioGroup(GroupTable):
    """
    A Django model representing a scenario group.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)

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




class PatentGroup(GroupTable):
    """
    A Django model representing a patent group.
    """
    patent_number = models.CharField(max_length=30)

    def __str__(self):
        return f"PatentGroup {self.id}: {self.patent_number}"

class Patent(DataTable):
    patent_group = models.ForeignKey(PatentGroup, on_delete=models.CASCADE) 
    remark = models.TextField()
    abstract = models.TextField()
    priority_date = models.DateField()


class PatentTagGroup(GroupTable):
    """
    A Django model representing a patent tag group.
    """
    def __str__(self):
        return f"PatentTagGroup {self.id}"

class PatentTag(DataTable):
    patent_tag_group = models.ForeignKey(PatentTagGroup, on_delete=models.CASCADE) 
    text = models.CharField(max_length=255)
    alt_text1 = models.CharField(max_length=255)
    alt_text2 = models.CharField(max_length=255)
    alt_text3 = models.CharField(max_length=255)
    alt_text4 = models.CharField(max_length=255)
    alt_text5 = models.CharField(max_length=255)
    priority_date = models.DateField()
    

class PatentClaimGroup(GroupTable):
    """
    A Django model representing a patent claim group.
    """
    patent_group = models.ForeignKey(PatentGroup, on_delete=models.CASCADE) 
    def __str__(self):
        return f"PatentClaimGroup {self.id}"
    
class PatentClaim(DataTable):
    patent_claim_group = models.ForeignKey(PatentClaimGroup, on_delete=models.CASCADE) 
    text = models.TextField()



class SapNumber(ReferenceTable):
  sap_number = models.CharField(max_length=255)

class ContractGroup(GroupTable):
    """
    A Django model representing a contract group.
    """
    contract_number = models.CharField(max_length=255)
    contract_date = models.DateTimeField()

    class Meta:
        unique_together = ('contract_number', 'contract_date')

    def __str__(self):
        return f"ContractGroup {self.id}"    
    
class Contract(DataTable):
    contract_group = models.ForeignKey(ContractGroup, on_delete= models.CASCADE)
    description = models.TextField()


class PartGroup(GroupTable):
    """
    A Django model representing a part group.
    """
    def __str__(self):
        return f"PartGroup {self.id}"
    
class Part(DataTable):

    part_group = models.ForeignKey(PartGroup, on_delete= models.CASCADE)


class PartRecipient(ReferenceTable):
    """
    A Django model representing the part recipient .
    """
    recipient_number = models.CharField(max_length=255)  

    def __str__(self):
        return self.recipient_number

class PartSoldGroup(GroupTable):
    """
    A Django model representing a part sold group.
    """
    part_recipient = models.ForeignKey(PartRecipient, on_delete= models.CASCADE)
    customer_part_number_sap = models.CharField(max_length=255)

    class Meta:
        unique_together = ('part_recipient', 'customer_part_number_sap')

    def __str__(self):
        return f"PartSoldGroup {self.id}"
    
class PartSold(DataTable):
    sap_number = models.ForeignKey(SapNumber, on_delete= models.CASCADE)
    part_sold_group = models.ForeignKey(PartSoldGroup, on_delete= models.CASCADE)
    customer_part_number = models.CharField(max_length=255)
    part_group = models.ManyToManyField(PartGroup,blank=False) 
    customer_plant = models.ForeignKey(CustomerPlant, on_delete= models.CASCADE)
    contract_group = models.ForeignKey(ContractGroup, on_delete= models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete= models.CASCADE)
    description = models.TextField()
    validity_start_date = models.DateTimeField()
    validity_end_date = models.DateTimeField()
    cbd_date = models.DateTimeField()


class PartSoldPriceType(ReferenceTable):
    name = models.CharField(max_length=255)

class Source(ReferenceTable):
    name = models.CharField(max_length=255) 

class SavingUnit(ReferenceTable):
    name = models.CharField(max_length=255) 

class PartSoldMaterialType(ReferenceTable):
    name = models.CharField(max_length=255)

class PartSoldMaterialPriceType(ReferenceTable):
    name = models.CharField(max_length=255)

class PartSoldPriceGroup(GroupTable):
    """
    A Django model representing a part sold price group.
    """
    part_sold = models.ForeignKey(PartSold, on_delete= models.CASCADE)
    part_sold_price_type = models.ForeignKey(PartSoldPriceType, on_delete= models.CASCADE)

    class Meta:
        unique_together = ('part_sold', 'part_sold_price_type')

    def __str__(self):
        return f"PartSoldPriceGroup {self.id}"
    
class PartSoldPrice(DataTable):
    part_sold_price_group = models.ForeignKey(PartSoldPriceGroup, on_delete= models.CASCADE)
    value = models.FloatField()
    saveable = models.FloatField()

class PartSoldCustomerPriceGroup(GroupTable):
    """
    A Django model representing a part sold customer price group.
    """
    part_sold = models.ForeignKey(PartSold, on_delete= models.CASCADE)
    part_sold_price_type = models.ForeignKey(PartSoldPriceType, on_delete= models.CASCADE)
    price_date = models.DateTimeField()
    
    class Meta:
        unique_together = ('part_sold', 'part_sold_price_type', 'price_date')

    def __str__(self):
        return f"PartSoldCustomerPriceGroup {self.id}"
    
class PartSoldCustomerPrice(DataTable):
    part_sold_customer_price_group = models.ForeignKey(PartSoldCustomerPriceGroup, on_delete= models.CASCADE)
    value = models.FloatField()


class PartSoldUploadedPriceGroup(GroupTable):
    """
    A Django model representing a part sold uploaded price group.
    """
    part_sold = models.ForeignKey(PartSold, on_delete= models.CASCADE)
    validity_start_date = models.DateTimeField()
    
    class Meta:
        unique_together = ('part_sold', 'validity_start_date')

    def __str__(self):
        return f"PartSoldUploadedPriceGroup {self.id}"
    
class PartSoldUploadedPrice(DataTable):
    part_sold_uploaded_price_group = models.ForeignKey(PartSoldUploadedPriceGroup, on_delete= models.CASCADE)
    value = models.FloatField()
    lme_basis = models.FloatField()
    ecdp_basis = models.FloatField()
    billet_basis = models.FloatField()
    source = models.ForeignKey(Source, on_delete= models.CASCADE)
    description = models.TextField()


class PartSoldMaterialPriceGroup(GroupTable):
    """
    A Django model representing a part sold material price group.
    """
    part_sold = models.ForeignKey(PartSold, on_delete= models.CASCADE)
    part_sold_material_price_type = models.ForeignKey(PartSoldMaterialPriceType, on_delete= models.CASCADE)
    
    class Meta:
        unique_together = ('part_sold', 'part_sold_material_price_type')

    def __str__(self):
        return f"PartSoldMaterialPriceGroup {self.id}"
    
class PartSoldMaterialPrice(DataTable):
    part_sold_material_price_group = models.ForeignKey(PartSoldMaterialPriceGroup, on_delete= models.CASCADE)
    variable = models.BooleanField()
    basis = models.FloatField()
    use_gross_weight = models.BooleanField()
    saveable = models.BooleanField()


class PartSoldMaterialWeightGroup(GroupTable):
    """
    A Django model representing a part sold material weight group.
    """
    part_sold = models.ForeignKey(PartSold, on_delete= models.CASCADE)
    part_sold_material_type = models.ForeignKey(PartSoldMaterialType, on_delete= models.CASCADE)
    
    class Meta:
        unique_together = ('part_sold', 'part_sold_material_type')

    def __str__(self):
        return f"PartSoldMaterialWeightGroup {self.id}"
    
class PartSoldMaterialWeight(DataTable):
    part_sold_material_weight_group = models.ForeignKey(PartSoldMaterialWeightGroup, on_delete= models.CASCADE)
    gross_weight = models.FloatField()
    net_weight = models.FloatField()


class PartSoldPriceSavingGroup(GroupTable):
    """
    A Django model representing a part sold price saving group.
    """
    part_sold = models.ForeignKey(PartSold, on_delete= models.CASCADE)
    saving_date = models.DateTimeField()

    class Meta:
        unique_together = ('part_sold', 'saving_date')

    def __str__(self):
        return f"PartSoldPriceSavingGroup {self.id}"
    
class PartSoldPriceSaving(DataTable):
    part_sold_price_saving_group = models.ForeignKey(PartSoldPriceSavingGroup, on_delete= models.CASCADE)
    saving_rate = models.FloatField()
    saving_unit = models.ForeignKey(SavingUnit, on_delete= models.CASCADE)


# class PartPrice(DataTable):
#  pass
# ###############################################################################################################
# ##NEW TABLES

# class ProjectTimingGroup(GroupTable):
#     """
#     A Django model representing a project timing group.
#     """
#     def __str__(self):
#         return f"ProjectTimingGroup {self.id}"

# class ProjectTiming(DataTable):

#     project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)
#     project_timing_group = models.ForeignKey(ProjectTimingGroup, on_delete=models.CASCADE)
#     derivative_constellium_group = models.ForeignKey(DerivativeConstelliumGroup,on_delete=models.CASCADE)
#     process_step_group = models.ForeignKey(ProcessStepGroup, on_delete=models.CASCADE)
#     priority_date = models.DateField()
#     description = models.TextField()
#     #class = models.CharField(max_length=255) ## in DB : milestone, milestone...
#     name = models.CharField(max_length=255) ##in DB daten nur EOP & SOP

#     project_status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE) ##in DB status : open, open...
#     project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)  ##in DB type : customer, customer...


# class ProjectIssueGroup(GroupTable):
#     """
#     A Django model representing a project issue group.
#     """
#     def __str__(self):
#         return f"ProjectIssueGroup {self.id}"

# class ProjectIssue(DataTable):

#     project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)
#     project_issue_group = models.ForeignKey(ProjectIssueGroup, on_delete=models.CASCADE)
#     description = models.TextField()
#     assignment = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)

#     priority = models.IntegerField()
#     traffic_light = models.IntegerField()


# ##PART  ##########################

 
# class PartPriceGroup(GroupTable):
#     """
#     A Django model representing a part price group.
#     """
#     def __str__(self):
#         return f"PartPriceGroup {self.id}"
    
# class PartPrice(DataTable):
#  pass
# #     part_sold_group = models.ForeignKey(PartSoldGroup, on_delete= models.CASCADE)
# #     cbd_date =
# #     validity_start_date = 
# #     validity_end_date = 
# #     raw_material_cost =
# #     value_add_without =
# #     value_add_with =
# #     value_add_without_saveable = 
# #     value_add_with_saveable = 
# #     price_net_weight = 
# #     price_gross_weight = 
# #     price_steel_weight =
# #     price_other_weight =
# #     variable_lme =
# #     variable_ecdp =
# #     variable_billet = 
# #     basis_lme =
# #     basis_ecdp =
# #     basis_billet = 
# #     lme_use_gross_weight =
# #     ecdp_use_gross_weight =
# #     billet_use_gross_weight =
# #     logistic_cost =
# #     sum_additional_cost = 


# class PartPriceCustomerGroup(GroupTable):
#     """
#     A Django model representing a part price customer group.
#     """
#     def __str__(self):
#         return f"PartPriceCustomerGroup {self.id}"
    
# class PartPriceCustomer(DataTable):

#     part_sold_group = models.ForeignKey(PartSoldGroup, on_delete= models.CASCADE)   
#     value_add = models.FloatField()
#     material_cost = models.ForeignKey(MaterialCost, on_delete= models.CASCADE)
#     price = models.FloatField()
#     automatic_upload = models.BooleanField()
#     price_date = models.DateField()
#     part_price_customer_group = models.ForeignKey(PartPriceCustomerGroup, on_delete= models.CASCADE)


# class PartPriceSavingGroup(GroupTable):
#     """
#     A Django model representing a part price saving group.
#     """
#     def __str__(self):
#         return f"PartPriceSavingGroup {self.id}"
    
# class PartPriceSaving(DataTable):

#     part_price_saving_group = models.ForeignKey(PartPriceSavingGroup, on_delete= models.CASCADE)
#     part_price = models.ForeignKey(PartPrice, on_delete= models.CASCADE)
#     valid_from = models.DateField()
#     saving = models.FloatField()
#     #unit = 

# class PartType(ReferenceTable):
#     name_csg = models.CharField(max_length=255)
#     name_dag = models.CharField(max_length=255)
#     name_bmw = models.CharField(max_length=255)
#     name_psa = models.CharField(max_length=255)
#     name_vag = models.CharField(max_length=255)

# class PartPosition(ReferenceTable):
#     name = models.CharField(max_length=255)

# class PartReleaseStatus(ReferenceTable):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     release_hierarchy = models.IntegerField	




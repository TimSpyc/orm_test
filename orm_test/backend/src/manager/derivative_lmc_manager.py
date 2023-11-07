from django.db import models
from backend.models import GroupTable, DataTable, ExternalDataTable, RevisionLMC
from backend.src.auxiliary.manager import GeneralManager, ExternalDataManager
from datetime import datetime, date

class DerivativeLmcGroup(GroupTable):
    lmc_full_code = models.CharField(max_length=255, unique=True)
    lmc_model_code = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lmc_full_code', 'lmc_model_code'],
                name='unique_derivative_lmc_group'
            )
        ]

    def __str__(self):
        return f"{self.lmc_full_code} - {self.lmc_model_code}"

    @property
    def manager(self):
        return DerivativeLmcManager

class DerivativeLmc(DataTable):
    derivative_lmc_group = models.ForeignKey(DerivativeLmcGroup, on_delete=models.DO_NOTHING)
    revision_lmc = models.ForeignKey("RevisionLMC", on_delete=models.DO_NOTHING)
    region = models.CharField(max_length=255)
    trade_region = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    sales_group = models.ForeignKey("CustomerGroup", related_name='sales_groups', on_delete=models.DO_NOTHING)
    manufacturer = models.ForeignKey("CustomerGroup", related_name='manufacturers', on_delete=models.DO_NOTHING)
    local_make = models.ForeignKey("CustomerGroup", related_name='local_makes', on_delete=models.DO_NOTHING)
    local_model_line = models.CharField(max_length=255)
    local_program_code = models.CharField(max_length=255)
    local_production_model = models.CharField(max_length=255)
    global_make = models.ForeignKey("CustomerGroup", related_name='global_makes', on_delete=models.DO_NOTHING)
    global_production_model = models.CharField(max_length=255)
    gvw = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    plant = models.ForeignKey("CustomerPlantGroup", on_delete=models.DO_NOTHING)
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
    design_lead = models.ForeignKey("CustomerGroup", related_name='design_leads', on_delete=models.DO_NOTHING)
    design_lead_location = models.CharField(max_length=255)
    design_lead_country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.derivative_lmc_group} - {self.local_make} {self.local_model_line}"
    
    @property
    def group_object(self):
        return self.derivative_lmc_group
    

class DerivativeLmcManager(GeneralManager):

    group_model = DerivativeLmcGroup
    data_model = DerivativeLmc
    data_extension_model_list = []


class DerivativeLmcVolume(ExternalDataTable):
    derivative_lmc_group = models.ForeignKey(DerivativeLmcGroup, on_delete=models.DO_NOTHING)
    volume = models.PositiveIntegerField()
    volume_date = models.DateField()
    lmc_revision = models.ForeignKey("RevisionLMC", on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['derivative_lmc_group', 'volume_date', 'lmc_revision'],
                name='unique_derivative_lmc_volume'
            )
        ]

    def __str__(self):
        return f"""
            Derivative Volume {self.id}:
            {self.derivative_lmc_group.lmc_full_code} - {self.date}
            for lmc_revision: {self.lmc_revision}
        """

class DerivativeLmcVolumeManager(ExternalDataManager):
    database_model = DerivativeLmcVolume

    def __init__(
        self,
        group_id:int,
        search_date: datetime | None = None,
    ):

        super().__init__(
            search_date=search_date,
        )

        self.derivative_lmc_group_id = group_id

    @property
    def current_volume(self) -> list[dict]:

        max_lmc_revision_for_date = RevisionLMC.objects.filter(
            revision_date__lte=self.search_date
        ).latest()

        return self.getVolumeForLmcRev(max_lmc_revision_for_date.revision_date)
    
    def getVolumeForLmcRev(self, lmc_revision: date) -> list[dict]:
        """
        Retrieves volume data for a given lmc revision date.

        Args:
            lmc_revision (date): The LMC revision date.

        Returns:
            List[Dict]: A list of dictionaries containing volume and date.
        """
        lmc_revision = RevisionLMC.objects.get(revision_date=lmc_revision)

        return self.getData(
            **{
                'derivative_lmc_group_id': self.derivative_lmc_group_id,
                'date__lte': self.search_date,
                'lmc_revision': lmc_revision,
            },
            column_list=['volume', 'volume_date']
        )
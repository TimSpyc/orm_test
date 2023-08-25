from backend.src.auxiliary.manager import GeneralManager
from backend.models.abstract_models import GroupTable, DataTable, DataExtensionTable
from django.db import models

class CustomerPlantGroup(GroupTable):
    customer_group = models.ForeignKey("CustomerGroup", on_delete=models.DO_NOTHING)
    plant_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.customer_group}|{self.plant_name} ({self.id})"

    @property
    def manager(self):
        return CustomerPlantManager

class CustomerPlant(DataTable):
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    part_recipient_group = models.ManyToManyField("PartRecipientGroup",blank=False)
    customer_plant_group = models.ForeignKey(CustomerPlantGroup, on_delete=models.DO_NOTHING)

    @property
    def group(self):
        return self.customer_plant_group


class CustomerPlantManager(GeneralManager):
    group_model = CustomerPlantGroup
    data_model = CustomerPlant
    data_extension_model_list = []

    def __init__(self, customer_plant_group_id, search_date=None, use_cache=True):
        super().__init__(customer_plant_group_id, search_date, use_cache)

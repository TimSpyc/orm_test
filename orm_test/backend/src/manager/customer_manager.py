from backend.src.auxiliary.manager import GeneralManager
from backend.models.abstract_models import GroupTable, DataTable, DataExtensionTable
from django.db import models

class CustomerGroup(GroupTable):
    company_name = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.company_name} ({self.group_name})"
    
    class meta:
        unique_together = ('company_name', 'group_name')

    def manager(self, search_date, use_cache):
        return CustomerManager(self.id, search_date, use_cache)

class Customer(DataTable):
    customer_group = models.ForeignKey(CustomerGroup, on_delete=models.CASCADE)

    @property
    def group(self):
        return self.customer_group


class CustomerMaterialCondition(DataExtensionTable):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    part_sold_material_price_type = models.ForeignKey("PartSoldMaterialPriceType", on_delete= models.DO_NOTHING)
    month_range = models.IntegerField()
    month_offset = models.IntegerField()
    share_the_pain_factor = models.FloatField()
    validity_start_date = models.DateTimeField(null=True)
    validity_end_date = models.DateTimeField(null=True)

class CustomerManager(GeneralManager):
    group_model = CustomerGroup
    data_model = Customer
    data_extension_model_list = [CustomerMaterialCondition]

    def __init__(self, customer_group_id, search_date=None, use_cache=True):
        super().__init__(customer_group_id, search_date, use_cache)

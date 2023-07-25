from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager
from backend.models import PartSoldGroup, PartSoldPriceComponentType

class PartSoldCustomerPriceGroup(GroupTable):
    """
    A Django model representing a part sold customer price group.
    """
    part_sold_group = models.ForeignKey(PartSoldGroup, on_delete= models.DO_NOTHING)
    price_date = models.DateTimeField()
    
    class Meta:
        unique_together = ('part_sold', 'price_date')

    def __str__(self):
        return f"PartSoldCustomerPriceGroup {self.part_sold_group} {self.price_date}"
    
class PartSoldCustomerPrice(DataTable):
    part_sold_customer_price_group = models.ForeignKey(PartSoldCustomerPriceGroup, on_delete= models.DO_NOTHING)
    value = models.FloatField()

class PartSoldCustomerPriceComponent(DataExtensionTable):
    part_sold_customer_price = models.ForeignKey(PartSoldCustomerPrice, on_delete= models.DO_NOTHING)
    part_sold_price_component_type = models.ForeignKey(PartSoldPriceComponentType, on_delete= models.DO_NOTHING)


class PartSoldCustomerPriceManager(GeneralManager):
    group_model = PartSoldCustomerPriceGroup
    data_model = PartSoldCustomerPrice
    data_extension_models = [PartSoldCustomerPriceComponent]
    
    def __init__(self, part_sold_customer_price_group_id, search_date=None, use_cache=True):
        super().__init__(part_sold_customer_price_group_id, search_date, use_cache)
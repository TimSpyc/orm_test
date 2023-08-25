from django.db import models
from backend.models import GroupTable, DataTable, ReferenceTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager


class PartSoldPriceUploadGroup(GroupTable):
    part_sold_group = models.ForeignKey('PartSoldGroup', on_delete= models.CASCADE)
    valid_from = models.DateTimeField()

    class _Meta:
        unique_together = ('part_sold_group', 'valid_from')

    @property
    def manager(self):
        return PartSoldPriceUploadManager

    def __str__(self):
        return f"PartSoldPriceUploadGroup {self.id}"


class PartSoldPriceUpload(DataTable):
    part_sold_price_upload_group = models.ForeignKey(PartSoldPriceUploadGroup, on_delete= models.CASCADE)
    uploaded = models.DateTimeField()
    price = models.FloatField()
    description = models.TextField()
    source = models.CharField(max_length=255)

    @property
    def group(self):
        return self.part_sold_price_upload_group

    def __str__(self):
        return f"PartSoldPriceUpload {self.id}"


class PartSoldPriceUploadManager(GeneralManager):
    group_model = PartSoldPriceUploadGroup
    data_model = PartSoldPriceUpload
    data_extension_models = []
    
    def __init__(self, part_sold_price_upload_group_id, search_date=None, use_cache=True):
        super().__init__(part_sold_price_upload_group_id, search_date, use_cache)

    def uploadPriceToSap(self):
        pass
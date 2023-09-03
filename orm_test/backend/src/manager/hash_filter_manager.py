from django.db import models
from backend.models import ExternalDataTable
from backend.src.auxiliary.manager import ExternalDataManager
from datetime import datetime

class HashFilter(ExternalDataTable):
    hash_code = models.CharField(max_length=255, unique=True)
    filter_info = models.JSONField()

    def __str__(self):
        return f"{self.hash_code}"
    

class HashFilterManager(ExternalDataManager):
    database_model = HashFilter

    def __init__(
        self,
        hash_code:str,
        search_date: datetime | None = None,
    ):
        super().__init__(
            search_date=search_date,
        )

        self.hash_code = hash_code

    @property
    def filter_info(self):
        return self.database_model.objects.get(hash_code=self.hash_code)
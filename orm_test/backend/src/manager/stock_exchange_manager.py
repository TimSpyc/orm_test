from django.db import models
from backend.models import ExternalDataTable
from backend.src.auxiliary.manager import ExternalDataManager

class StockExchangeData(ExternalDataTable):
    stock_exchange_date = models.DateTimeField()
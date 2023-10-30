from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import StockExchangeDataManager

class StockExchangeInfo(GeneralInfo):
    base_url = 'stock_exchange_data'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = StockExchangeDataManager
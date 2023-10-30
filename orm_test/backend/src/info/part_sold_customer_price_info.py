from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import PartSoldCustomerPriceManager

class PartSoldCustomerPriceInfo(GeneralInfo):
    base_url = 'part_sold/customer_price'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = PartSoldCustomerPriceManager
from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import CustomerManager

class CustomerInfo(GeneralInfo):
    base_url = 'customer'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = CustomerManager
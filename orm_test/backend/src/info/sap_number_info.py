from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import SapNumberManager

class SapNumberInfo(GeneralInfo):
    base_url = 'sap_number'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = SapNumberManager
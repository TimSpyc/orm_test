from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import  CustomerPlantManager

class CustomerPlantInfo(GeneralInfo):
    base_url = 'customer_plant'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = CustomerPlantManager
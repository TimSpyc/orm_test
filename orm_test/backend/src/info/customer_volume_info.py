from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import CustomerVolumeManager

class CustomerVolumeInfo(GeneralInfo):
    base_url = 'customer_volume'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = CustomerVolumeManager
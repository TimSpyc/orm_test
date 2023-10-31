from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import HashFilterManager

class HashFilterInfo(GeneralInfo):
    base_url = 'hash_filter'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = HashFilterManager
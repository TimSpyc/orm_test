from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import NormManager

class NormInfo(GeneralInfo):
    base_url = 'norm'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = NormManager
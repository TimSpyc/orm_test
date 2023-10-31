from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import PartManager

class PartInfo(GeneralInfo):
    base_url = 'part'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = PartManager
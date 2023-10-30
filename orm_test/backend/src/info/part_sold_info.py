from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import PartSoldManager

class PartSoldInfo(GeneralInfo):
    base_url = 'part_sold'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = PartSoldManager
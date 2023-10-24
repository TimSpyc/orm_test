from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import PatentManager


class PatentInfo(GeneralInfo):
    base_url = 'patent'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = PatentManager

from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import AbsenceManager

class AbsenceInfo(GeneralInfo):
    base_url = 'absence'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = AbsenceManager
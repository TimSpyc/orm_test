from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ChangeRequestFeasibilityManager

class ChangeRequestFeasibilityInfo(GeneralInfo):
    base_url = 'change_request_feasibility'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ChangeRequestFeasibilityManager


from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ChangeRequestCostManager

class ChangeRequestCostInfo(GeneralInfo):
    base_url = 'change_request/cost_evaluation'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ChangeRequestCostManager
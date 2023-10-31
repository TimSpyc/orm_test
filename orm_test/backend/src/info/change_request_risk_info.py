from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ChangeRequestRiskManager

class ChangeRequestRiskInfo(GeneralInfo):
    base_url = 'change_request_risk_analysis'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ChangeRequestRiskManager

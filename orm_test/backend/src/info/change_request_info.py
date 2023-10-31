from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ChangeRequestManager

class ChangeRequestInfo(GeneralInfo):
    base_url = 'change_request'#TODO adapt frontend requests url
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ChangeRequestManager
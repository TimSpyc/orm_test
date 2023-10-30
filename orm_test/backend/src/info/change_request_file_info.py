from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ChangeRequestFileManager

class ChangeRequestFileInfo(GeneralInfo):
    base_url = 'change_request/file'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ChangeRequestFileManager
from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import PermissionMasterManager

class PermissionMasterInfo(GeneralInfo):
    base_url = 'permission_master'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = PermissionMasterManager
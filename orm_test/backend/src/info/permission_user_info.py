from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import PermissionUserManager

class PermissionUserInfo(GeneralInfo):
    base_url = 'permission_user'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = PermissionUserManager
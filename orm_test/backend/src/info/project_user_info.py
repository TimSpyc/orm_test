from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ProjectUserManager

class ProjectUserInfo(GeneralInfo):
    base_url = 'project_user' #TODO find a better url?
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ProjectUserManager
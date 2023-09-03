from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ProjectManager


class ProjectInfo(GeneralInfo):
    base_url = 'project'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ProjectManager

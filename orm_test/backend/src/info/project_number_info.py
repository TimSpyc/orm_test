from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ProjectNumberManager


class ProjectNumberInfo(GeneralInfo):
    base_url = 'project_number'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ProjectNumberManager

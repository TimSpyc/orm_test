from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ProjectStaffCostManager

def permissionFunction(request_info_dict, data_set_dict):
    return request_info_dict["request_user_id"] == data_set_dict["user_id"]

class ProjectStaffCostInfo(GeneralInfo):
    base_url = 'project_staff_cost'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ProjectStaffCostManager
    datasetPermissionFunction = permissionFunction


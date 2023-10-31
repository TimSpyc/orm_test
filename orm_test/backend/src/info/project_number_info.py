from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ProjectNumberManager, ProjectNumberFinancialOverviewManager


def serializeProjectNumberManager(project_number_manager_obj):
    project_number_group_id = project_number_manager_obj.group_id
    financial_overview_manager_obj = ProjectNumberFinancialOverviewManager(project_number_group_id)

    result_dict = {
        **dict(project_number_manager_obj),
       'project_number__financial_overview_list_of_dict': \
        financial_overview_manager_obj.project_number_financial_overview_list_of_dict,
    }

    return result_dict

    
class ProjectNumberInfo(GeneralInfo):
    base_url = 'project_number'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ProjectNumberManager
    serializerFunction  = serializeProjectNumberManager

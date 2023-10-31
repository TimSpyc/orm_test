from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ScenarioManager

class ScenarioInfo(GeneralInfo):
    base_url = 'scenario'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ScenarioManager
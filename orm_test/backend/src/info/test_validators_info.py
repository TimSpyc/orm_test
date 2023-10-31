from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import TestManagerManager

class TestValidatorsInfo(GeneralInfo):
    base_url = 'test_manager'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = TestManagerManager
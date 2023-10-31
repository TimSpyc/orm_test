from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import DerivativeLmcManager

class DerivativeLmcInfo(GeneralInfo):
    base_url = 'derivative_lmc'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = DerivativeLmcManager
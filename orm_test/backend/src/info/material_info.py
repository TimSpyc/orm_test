from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import MaterialManager

class MaterialInfo(GeneralInfo):
    base_url = 'material'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = MaterialManager
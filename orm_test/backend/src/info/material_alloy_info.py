from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import MaterialAlloyManager

class MaterialAlloyInfo(GeneralInfo):
    base_url = 'material_alloy'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = MaterialAlloyManager
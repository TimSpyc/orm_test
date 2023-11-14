from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import MaterialAlloyTreatmentManager

class MaterialAlloyTreatmentInfo(GeneralInfo):
    base_url = 'material_alloy_treatment'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = MaterialAlloyTreatmentManager
from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import CrossSectionManager

class CrossSectionInfo(GeneralInfo):
    base_url = 'cross_section'
    allowed_method_list = ['GET_detail', 'GET_list']
    required_permission_list = []
    manager = CrossSectionManager
from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import TimeCorrectionManager

class TimeCorrectionInfo(GeneralInfo):
    base_url = 'time_correction'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = TimeCorrectionManager

class TimeCorrectionInfo(GeneralInfo):
    base_url = 'verify/time_correction'
    allowed_method_list = ['GET_detail']
    required_permission_list = []
    manager = TimeCorrectionManager
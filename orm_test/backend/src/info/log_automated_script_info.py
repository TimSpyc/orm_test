from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import LogAutomatedScriptManager

class LogAutomatedScriptInfo(GeneralInfo):
    base_url = 'log_table' #"user/script_monitoring/" url in react_frontend
    allowed_method_list = ['GET_list']
    required_permission_list = []
    manager = LogAutomatedScriptManager
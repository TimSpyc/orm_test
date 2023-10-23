from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import ChangeRequestManager
from backend.src.manager import ChangeRequestCostManager
from backend.src.manager import ChangeRequestFeasibilityManager
from backend.src.manager import ChangeRequestRiskManager
from backend.src.manager import ChangeRequestFileManager

# ChangeRequestManager : ----------------------------------------------------- #
class ChangeRequestSelectionInfo(GeneralInfo):
    base_url = 'change_request'#TODO adapt frontend requests url
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ChangeRequestManager

class ChangeRequestSendKickOffEmailInfo(GeneralInfo):
    base_url = 'change_request/send_kick_off_email'
    allowed_method_list = ['PUT']
    required_permission_list = []
    manager = ChangeRequestManager

# ChangeRequestFileManager : ------------------------------------------------- #
class ChangeRequestFileInfo(GeneralInfo):
    base_url = 'change_request/file'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ChangeRequestFileManager
    
# ChangeRequestCostManager : ------------------------------------------------- #
class ChangeRequestCostInfo(GeneralInfo):
    base_url = 'change_request/cost_evaluation'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ChangeRequestCostManager

# ChangeRequestFeasibilityManager : ------------------------------------------ #
class ChangeRequestFeasibilityInfo(GeneralInfo):
    base_url = 'change_request/feasibility'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ChangeRequestFeasibilityManager

# ChangeRequestRiskManager : ------------------------------------------------- #
class ChangeRequestRiskInfo(GeneralInfo):
    base_url = 'change_request/risk_analysis'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = ChangeRequestRiskManager




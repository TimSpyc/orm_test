from backend.src.info import *
from backend.src.info.reference_model_info import createReferenceUrls

info_list = [
    ProjectInfo,
    ProjectNumberInfo,
    DerivativeConstelliumInfo,
    ProjectStaffCostInfo,
    ChangeRequestSelectionInfo,
    ChangeRequestSendKickOffEmailInfo,
    ChangeRequestCostInfo,
    ChangeRequestFeasibilityInfo,
    ChangeRequestRiskInfo,
    ChangeRequestFileInfo,
]

def createInfoUrls():
    urlpatterns = []
    for info_class in info_list:
        urlpatterns += info_class.getUrlList()
    return urlpatterns

urlpatterns = createInfoUrls() + createReferenceUrls()


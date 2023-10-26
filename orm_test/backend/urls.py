from backend.src.info import *
from backend.src.info.reference_model_info import createReferenceUrls

info_list = [
    AbsenceInfo,
    AssetItemInfo,
    AssetItemSiteConnectionInfo,
    AssetLayoutInfo,
    AssetSiteInfo,
    ChangeRequestSelectionInfo,
    ChangeRequestSendKickOffEmailInfo,
    ChangeRequestCostInfo,
    ChangeRequestFeasibilityInfo,
    ChangeRequestRiskInfo,
    ChangeRequestFileInfo,
    DerivativeConstelliumInfo,  
    PatentInfo,
    PermissionMasterInfo,
    PermissionUserInfo,
    ProjectInfo,
    ProjectNumberInfo,
    ProjectStaffCostInfo,
    TimeCorrectionInfo,
    TimeCorrectionInfo,
  
]

def createInfoUrls():
    urlpatterns = []
    for info_class in info_list:
        urlpatterns += info_class.getUrlList()
    return urlpatterns

urlpatterns = createInfoUrls() + createReferenceUrls()


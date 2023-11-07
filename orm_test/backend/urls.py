from backend.src.info import *
from backend.src.info.reference_model_info import createReferenceUrls

info_list = [
    AbsenceInfo,
    AssetItemInfo,
    AssetItemSiteConnectionInfo,
    AssetLayoutInfo,
    AssetSiteInfo,
    BillOfMaterialInfo,
    ChangeRequestCostInfo,
    ChangeRequestFeasibilityInfo,
    ChangeRequestFileInfo,
    ChangeRequestInfo,
    ChangeRequestRiskInfo,
    CrossSectionInfo,
    CustomerInfo,
    CustomerPlantInfo,
    CustomerVolumeInfo,
    DerivativeConstelliumInfo, 
    DerivativeLmcInfo,
    FileInfo,
    HashFilterInfo,
    LogAutomatedScriptInfo,
    MaterialAlloyInfo,
    MaterialAlloyTreatmentInfo,
    MaterialInfo,
    NormInfo,
    PartInfo,
    PartSoldContractInfo,
    PartSoldCustomerPriceInfo,
    PartSoldInfo,
    PartSoldPriceUploadInfo,
    PatentInfo,
    PermissionMasterInfo,
    PermissionUserInfo,
    ProjectInfo,
    ProjectNumberInfo,
    ProjectStaffCostInfo,
    ProjectUserInfo,
    SapNumberInfo,
    StockExchangeDataInfo,
    TimeCorrectionInfo,
]

def createInfoUrls():
    urlpatterns = []
    for info_class in info_list:
        urlpatterns += info_class.getUrlList()
    return urlpatterns

urlpatterns = createInfoUrls() + createReferenceUrls()


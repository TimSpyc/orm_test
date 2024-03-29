from .abstract_models import GroupTable, ReferenceTable, DataTable, DataExtensionTable, ExternalDataTable
from backend.src.auxiliary.new_cache import DatabaseCache
from .reference_models import *

from backend.src.manager.absence_manager import Absence, AbsenceGroup
from backend.src.manager.asset_item_manager import AssetItem, AssetItemGroup
from backend.src.manager.asset_item_site_connection_manager import AssetItemSiteConnection, AssetItemSiteConnectionGroup
from backend.src.manager.asset_layout_manager import AssetLayout, AssetLayoutGroup
from backend.src.manager.asset_site_manager import AssetSite, AssetSiteGroup
from backend.src.manager.bill_of_material_manager import BillOfMaterial, BillOfMaterialGroup, BillOfMaterialStructure
from backend.src.manager.change_request_manager import ChangeRequest, ChangeRequestGroup
from backend.src.manager.change_request_file_manager import ChangeRequestFile, ChangeRequestFileGroup
from backend.src.manager.change_request_feasibility_manager import ChangeRequestFeasibility, ChangeRequestFeasibilityGroup
from backend.src.manager.change_request_cost_manager import ChangeRequestCost, ChangeRequestCostGroup
from backend.src.manager.change_request_risk_manager import ChangeRequestRisk, ChangeRequestRiskGroup
from backend.src.manager.cross_section_manager import CrossSection, CrossSectionGroup
from backend.src.manager.customer_manager import Customer, CustomerGroup, CustomerMaterialCondition
from backend.src.manager.customer_volume_manager import CustomerVolume, CustomerVolumeGroup, CustomerVolumeVolume
from backend.src.manager.customer_plant_manager import CustomerPlant, CustomerPlantGroup
from backend.src.manager.derivative_constellium_manager import DerivativeConstellium, DerivativeConstelliumGroup, DerivativeConstelliumDerivativeLmcConnection
from backend.src.manager.derivative_lmc_manager import DerivativeLmc, DerivativeLmcGroup, DerivativeLmcVolume
from backend.src.manager.file_manager import File, FileGroup
from backend.src.manager.material_alloy_manager import MaterialAlloy, MaterialAlloyGroup
from backend.src.manager.material_alloy_treatment_manager import MaterialAlloyTreatment, MaterialAlloyTreatmentGroup
from backend.src.manager.material_manager import Material, MaterialGroup
from backend.src.manager.norm_manager import Norm, NormGroup
from backend.src.manager.part_manager import Part, PartGroup
from backend.src.manager.part_recipient_manager import PartRecipient, PartRecipientGroup
from backend.src.manager.part_sold_contract_manager import PartSoldContract, PartSoldContractGroup
from backend.src.manager.part_sold_customer_price_manager import PartSoldCustomerPrice, PartSoldCustomerPriceGroup, PartSoldCustomerPriceComponent
from backend.src.manager.part_sold_manager import PartSold, PartSoldGroup, PartSoldPriceComponent, PartSoldMaterialPriceComponent, PartSoldMaterialWeight, PartSoldSaving
from backend.src.manager.part_sold_price_upload_manager import PartSoldPriceUpload, PartSoldPriceUploadGroup
from backend.src.manager.patent_manager import Patent, PatentGroup, PatentClaim
from backend.src.manager.permission_master_manager import PermissionMaster, PermissionMasterGroup
from backend.src.manager.permission_user_manager import PermissionUser, PermissionUserGroup
from backend.src.manager.project_manager import Project, ProjectGroup
from backend.src.manager.project_number_manager import ProjectNumber, ProjectNumberGroup, ProjectNumberFinancialOverview
from backend.src.manager.project_staff_cost_manager import ProjectStaffCost, ProjectStaffCostGroup
from backend.src.manager.project_user_manager import ProjectUser, ProjectUserGroup
from backend.src.manager.sap_number_manager import SapNumber, SapNumberGroup
from backend.src.manager.stock_exchange_data_manager import StockExchangeData
from backend.src.manager.time_correction_manager import TimeCorrection, TimeCorrectionGroup
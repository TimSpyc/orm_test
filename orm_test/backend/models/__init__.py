from .abstract_models import GroupTable, ReferenceTable, DataTable, DataExtensionTable, ExternalDataTable
from .caching_models import CacheManager, CacheIntermediate
from .reference_models import *

from backend.src.manager.project_manager import Project, ProjectGroup
from backend.src.manager.sap_number_manager import SapNumber, SapNumberGroup
from backend.src.manager.cross_section_manager import CrossSection, CrossSectionGroup
from backend.src.manager.norm_manager import Norm, NormGroup
from backend.src.manager.part_sold_manager import PartSold, PartSoldGroup
from backend.src.manager.part_manager import Part, PartGroup
from backend.src.manager.part_recipient_manager import PartRecipient, PartRecipientGroup
from backend.src.manager.material_manager import Material, MaterialGroup
from backend.src.manager.material_alloy_manager import MaterialAlloy, MaterialAlloyGroup
from backend.src.manager.material_alloy_treatment_manager import MaterialAlloyTreatment, MaterialAlloyTreatmentGroup
from backend.src.manager.part_sold_contract_manager import PartSoldContract, PartSoldContractGroup
from backend.src.manager.customer_manager import Customer, CustomerGroup
from backend.src.manager.customer_plant_manager import CustomerPlant, CustomerPlantGroup
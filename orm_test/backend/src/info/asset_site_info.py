from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import AssetSiteManager

class AssetSiteInfo(GeneralInfo):
    base_url = 'asset_site'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = AssetSiteManager
    
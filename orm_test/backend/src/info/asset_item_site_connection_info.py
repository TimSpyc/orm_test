from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import AssetItemSiteConnectionManager

class AssetItemSiteConnectionInfo(GeneralInfo):
    base_url = 'asset_item_site_connection'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = AssetItemSiteConnectionManager
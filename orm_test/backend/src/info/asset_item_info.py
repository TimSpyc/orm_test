from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import AssetItemManager

class AssetItemInfo(GeneralInfo):
    base_url = 'asset_item'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = AssetItemManager
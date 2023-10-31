from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import AssetLayoutManager

class AssetLayoutInfo(GeneralInfo):
    base_url = 'asset_layout'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = AssetLayoutManager
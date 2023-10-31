from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import PartSoldPriceUploadManager

class PartSoldPriceUploadInfo(GeneralInfo):
    base_url = 'part_sold_price_upload'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = PartSoldPriceUploadManager
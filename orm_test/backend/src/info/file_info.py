from backend.src.auxiliary.info import GeneralInfo
from backend.src.manager import FileManager

class FileInfo(GeneralInfo):
    base_url = 'file/upload_file/'
    allowed_method_list = ['POST']
    required_permission_list = []
    manager = FileManager
from backend.src.auxiliary.info import GeneralInfo, addPrefix
from backend.src.manager import DerivativeConstelliumManager


class DerivativeConstelliumInfo(GeneralInfo):
    base_url = 'derivative_constellium'
    allowed_method_list = ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list = []
    manager = DerivativeConstelliumManager
    serializerFunction = lambda derivative_constellium_manager_obj: {
        **dict(derivative_constellium_manager_obj), 
        **addPrefix(
            dict(
                derivative_constellium_manager_obj.\
                project_manager
            ),
            'project'
        ),
    }


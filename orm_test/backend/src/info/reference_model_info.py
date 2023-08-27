
import inspect
from backend.models import reference_models
from backend.src.auxiliary.info import GeneralInfo

def createReferenceUrls():
    url_list = []
    reference_model_list = getReferenceModels()
    for reference_model in reference_model_list:
        url_list += createUrlsForReferenceModel(reference_model)
    return url_list

def getReferenceModels():
    reference_model_list = []
    for _, reference_model in inspect.getmembers(reference_models):
        is_class = inspect.isclass(reference_model)
        if not is_class:
            continue
        is_reference_model = reference_model.__name__ == 'ReferenceTable'
        if is_reference_model:
            continue
        is_subclass = issubclass(reference_model, reference_models.ReferenceTable)
        if is_subclass:
            reference_model_list.append(reference_model)
    return reference_model_list

def createUrlsForReferenceModel(reference_model):
    info_class = type(
        f'{reference_model.__name__}Info',
        (GeneralInfo,),
        {
            'allowed_method_list': ['GET_detail', 'GET_list'],
            'base_url': f'reference/{reference_model.__name__}',
            'required_permission_list': [],
            'detail_key_dict': {'id': 'int'},
            'getList': lambda self: reference_model.objects.all().values(),
            'getDetail': getDetailFunction(reference_model),
        }
    )
    return info_class.getUrlList()

def getDetailFunction(reference_model):
    def getDetail(self):
        query = reference_model.objects.filter(id=self.identifier['id'])
        result = query.values()
        if result:
            return result[0]
        else:
            return {}
    return getDetail
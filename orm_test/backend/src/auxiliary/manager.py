from exceptions import NonExistentGroupError
import re
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

def transferToSnakeCase(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def updateCache(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.updateCache()

        return result
    return wrapper

def createCache(func):
    def wrapper(cls, *args, **kwargs):
        result = func(cls, *args, **kwargs)
        result.updateCache()

        return result
    return wrapper


class GeneralManager:
    def __init__(self, group_id, group_model, data_model, date=None, use_cache=True):
        group_obj = self.__getGroupObject(group_id, group_model, use_cache)
        data_obj = self.__getDataObject(group_obj, data_model, date, use_cache)

        self.__group_obj = group_obj
        self.__data_obj = data_obj

        self.id = data_obj.id
        self.group_id = group_obj.id
        self.creator_user_id = data_obj.creator.id
        self.creator = data_obj.creator
        self.active = data_obj.active
        self.date = data_obj.date
        self.search_date = None

        return group_obj, data_obj

    @staticmethod
    def __getGroupObject(group_id, group_model, use_cache):
        cached_group_obj = None
        if use_cache:
            cached_group_obj = cache.get(f"{group_model.__name__}|{group_id}")
        if cached_group_obj:
            return cached_group_obj
        else:
            try:
                return group_model.objects.get(id=group_id)
            except ObjectDoesNotExist:
                raise NonExistentGroupError(
                    f"{group_model.__name__} with id {group_id} does not exist")

    @staticmethod
    def __getDataObject(group_obj, data_model, date, use_cache):
        if use_cache:
            cached_data_obj = cache.get(f"{data_model.__name__}|{group_obj.id}|{date}")
            if cached_data_obj:
                return cached_data_obj
        if date is None:
            data_obj = data_model.objects.filter(
                **{transferToSnakeCase(group_obj.__class__.__name__): group_obj}
            ).latest('id')
        else:
            data_obj = data_model.objects.filter(
                **{transferToSnakeCase(group_obj.__class__.__name__): group_obj, 'date__lte': date}
            ).latest('id')
        
        return data_obj
    
    @staticmethod
    def __setDataObjectCache(data_obj, group_obj, date):
        cache_key = f"{data_obj.__class__.__name__}|{group_obj.id}|{date}"
        cache.set(cache_key, data_obj)

    @staticmethod
    def __setGroupObjectCache(group_obj):
        cache_key = f"{group_obj.__class__.__name__}|{group_obj.id}"
        cache.set(cache_key, group_obj)

    def updateCache(self):
        self.__setDataObjectCache(
            self._GeneralManager__data_obj,
            self._GeneralManager__group_obj,
            self.search_date
        )

        self.__setGroupObjectCache(self._GeneralManager__group_obj)

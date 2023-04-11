from exceptions import NonExistentGroupError
import re
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from backend.models import CacheEntry

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
    def __new__(cls, group_id, group_model, data_model, date=None, use_cache=True):
        if use_cache:
            manager_name = cls.__name__
            if date is None:
                cached_group_obj = cache.get(f"{manager_name}|{group_id}")
            cached_instance = CacheEntry.objects.get_cache_data(manager_name, data_model, group_id, date)
            if cached_instance:
                return cached_instance

        instance = super().__new__(cls)
        instance.__init__(group_id, group_model, data_model, date)
        CacheEntry.objects.set_cache_data(manager_name, group_id, instance, instance.date)
        return instance

    def __init__(self, group_id, group_model, data_model, date=None):
        group_obj = self.__getGroupObject(group_id, group_model)
        data_obj = self.__getDataObject(group_obj, data_model, date)

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
    def __getGroupObject(group_id, group_model):
        try:
            return group_model.objects.get(id=group_id)
        except ObjectDoesNotExist:
            raise NonExistentGroupError(
                f"{group_model.__name__} with id {group_id} does not exist")

    @staticmethod
    def __getDataObject(group_obj, data_model, date):
        if date is None:
            data_obj = data_model.objects.filter(
                **{transferToSnakeCase(group_obj.__class__.__name__): group_obj}
            ).latest('id')
        else:
            data_obj = data_model.objects.filter(
                **{transferToSnakeCase(group_obj.__class__.__name__): group_obj, 'date__lte': date}
            ).latest('id')
        
        return data_obj
    
    def __setManagerObjectDjangoCache(self):
        cache_key = f"{self.__class__.__name__}|{self.group_id}"
        cache.set(cache_key, self)

    def updateCache(self):
        if self.search_date is None:
            self.__setManagerObjectDjangoCache()
        CacheEntry.objects.set_cache_data(self.__class__.__name__, self.group_id, self, self.date)

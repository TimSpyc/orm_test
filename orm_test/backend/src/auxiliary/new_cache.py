from django.db import models
from django.db.models import Q
from hashlib import md5
import json, pickle
from datetime import datetime
from django.core.cache import cache
import inspect

class DatabaseCache(models.Model):

    id_string = models.CharField(max_length=100)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    data = models.BinaryField()

    class Meta:
        unique_together = ('id_string', 'start_date', 'end_date')

    @classmethod
    def getCacheData(
        cls,
        id_string: str,
        search_date: datetime | None = None
    ) -> object | None:
        
        if search_date is None:
            search_date = datetime.now()
        try:
            result = cls.objects.filter(
                Q(start_date__lte=search_date, end_date__gte=search_date) | 
                Q(start_date__lte=search_date, end_date__isnull=True) |
                Q(start_date__isnull=True, end_date__isnull=True),
                id_string=id_string,
            )
            if result.exists():
                entry = result.first()
                return pickle.loads(entry.data)
        except cls.DoesNotExist:
            pass
        return None
    
    @classmethod
    def setCacheData(
        cls,
        id_string: str,
        data: object,
    ) -> None:
        if hasattr(data, '_start_date'):
            start_date = data._start_date
        else:
            start_date = None
        if hasattr(data, '_end_date'):
            end_date = data._end_date
        else:
            end_date = None
        entry, _ = cls.objects.get_or_create(
            id_string=id_string,
            start_date=start_date,
            end_date=end_date
        )
        entry.data=pickle.dumps(data)
        entry.save()

    @classmethod
    def updateCacheEndDate(
        cls,
        id_string: str,
        data: object,
    ) -> None:
        if hasattr(data, '_start_date'):
            start_date = data._start_date
        else:
            start_date = None
        
        new_end_date = datetime.now()
        if hasattr(data, '_end_date'):
            data._end_date = new_end_date

        cached_object_list = cls.objects.filter(
            id_string=id_string,
            start_date=start_date,
            end_date=None
        )
        if cached_object_list.exists():
            entry = cached_object_list.first()
            entry.end_date = new_end_date
            entry.data=pickle.dumps(data)
            entry.save()


class RAMCache:
    @staticmethod
    def getCacheData(
        id_string: str,
    ) -> object | None:
        return cache.get(id_string)
    
    @staticmethod
    def setCacheData(
        id_string: str,
        data: object,
    ) -> None:
        is_newest_data = (
            (not hasattr(data, '_end_date'))
            or data._end_date is None
            or id_string == 'CacheHandler'
        )

        if is_newest_data:
            cache.set(id_string, data)
    
    @staticmethod
    def invalidateCache(
        id_string: str,
    ) -> None:
        cache.delete(id_string)


class CacheObserver:

    def __init__(self, id_string: str) -> None:
        self.id_string = id_string
        self.dependent_objects = {}

    def add(
        self,
        dependent_object: object,
    ) -> None:
        dependent_object_id_string = getIdString(dependent_object)
        if dependent_object_id_string not in self.dependent_objects:
            self.dependent_objects[dependent_object_id_string].append(
                dependent_object
            )

    def invalidate(self) -> None:
        for id_string, dependent_object in self.dependent_objects.items():
            RAMCache.invalidateCache(id_string)
            DatabaseCache.updateCacheEndDate(id_string, dependent_object)
        self.destroy()

    def destroy(self) -> None:
        CacheHandler.removeObserver(self.id_string)


class CacheHandler:
    __instance = None
    cache_observer_dict = {}

    def __new__(cls) -> "CacheHandler":
        """
        Create a new instance of CacheHandler if one does not already exist.
        """
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cache_observer_dict = RAMCache.getCacheData('CacheHandler')
            if cache_observer_dict is None:
                DatabaseCache.objects.all().delete()
                cache_observer_dict = {}
            cls.__instance.cache_observer_dict = cache_observer_dict
        return cls.__instance

    @classmethod
    def addGeneralManagerObjectToCache(
        cls,
        manager: object
    ) -> None:
        self = cls()
        self._createCache(manager)

    @classmethod
    def addDependentObjectToCache(
        cls,
        dependency_obj_list: object,
        dependent_obj: object
    ) -> None:
        self = cls()
        for dependency_obj in dependency_obj_list:
            self._addDependentObjectToObserver(dependency_obj, dependent_obj)
        self._createCache(dependent_obj)

    @staticmethod
    def getObjectFromCache(
        identification_dict: dict,
        search_date: datetime | None = None
    ):
        id_string, is_managed_object = getIdString(identification_dict)
        data = None
        if not is_managed_object:
            return data
        if (search_date is None or
            search_date > datetime.now() - datetime.timedelta(second=5)
        ):
            data = RAMCache.getCacheData(id_string)
        if data is None:
            data = DatabaseCache.getCacheData(id_string, search_date)
            if data is not None and search_date is None:
                RAMCache.setCacheData(id_string, data)
        return data

    @classmethod
    def invalidateCache(
        cls,
        object: object
    ) -> None:
        self = cls()
        id_string, is_managed_object = getIdString(object._identification_dict)
        if is_managed_object:
            RAMCache.invalidateCache(id_string)
            DatabaseCache.updateCacheEndDate(id_string, object)
        if id_string in self.cache_observer_dict:
            self.cache_observer_dict[id_string].invalidate()
            RAMCache.setCacheData('CacheHandler', self.cache_observer_dict)

    @classmethod
    def removeObserver(cls, id_string: str) -> None:
        self = cls()
        del self.cache_observer_dict[id_string]
        RAMCache.setCacheData('CacheHandler', self.cache_observer_dict)


    def _addDependentObjectToObserver(
        self,
        dependency_obj: object,
        dependent_obj: object
    ) -> None:
        id_string, _ = getIdString(dependency_obj._identification_dict)
        if id_string not in self.cache_observer_dict:
            self.cache_observer_dict[id_string] = CacheObserver(id_string)
        self.cache_observer_dict[id_string].add(dependent_obj)
        RAMCache.setCacheData('CacheHandler', self.cache_observer_dict)

    def _createCache(
        self,
        data: object
    ) -> None:
        id_string, is_managed_object = getIdString(data._identification_dict)
        if is_managed_object:
            DatabaseCache.setCacheData(id_string, data)
            RAMCache.setCacheData(id_string, data)

def getIdString(
        general_object: object
    ) -> str:
    """
    Convert an identification_dict into a JSON string, with keys sorted. This
    wil create a unique string for each identification_dict, which can be used
    as a key in a cache.
    """
    is_object = isinstance(
        general_object,
        object
    )
    is_class = isinstance(
        general_object,
        type
    )
        
    if is_object:
        return getIdStringFromDict(general_object._identification_dict), is_object
    elif is_class: # is not an instance but the class itself
        return general_object.__name__, is_object


def getIdStringFromDict(
    identification_dict: dict
) -> str:
    """
    Convert an identification_dict into a JSON string, with keys sorted. This
    wil create a unique string for each identification_dict, which can be used
    as a key in a cache.
    """
    id_json = json.dumps(identification_dict, sort_keys=True, cls=DateTimeEncoder)
    return md5(id_json.encode()).hexdigest()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def addDependencyToFunctionCaller(
    dependency: object
) -> None:
    """
    Identifies the caller of the function that called this function. If the
    caller is a method, returns the instance of the class that called the
    method.
    """
    frame = inspect.currentframe()
    try:
        frame = frame.f_back.f_back
        instance = recursiveSearchForIntermediateOrInfo(frame)
        if instance is not None:
            instance._dependencies.append(dependency)
    finally:
        del frame # important to avoid memory leak!
    
def recursiveSearchForIntermediateOrInfo(frame):
    from backend.src.auxiliary.info import GeneralInfo
    from backend.src.auxiliary.intermediate import GeneralIntermediate

    if 'self' in frame.f_locals:
        instance = frame.f_locals['self']
        if isinstance(instance, (GeneralIntermediate, GeneralInfo)):
            return instance
        return recursiveSearchForIntermediateOrInfo(frame.f_back)
    return None

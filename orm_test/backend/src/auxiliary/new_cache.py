from django.db import models
from django.db.models import Q
from hashlib import md5
import json, pickle
from datetime import datetime
from backend.src.auxiliary import GeneralIntermediate, GeneralManager, GeneralInfo
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
    ) -> GeneralIntermediate | GeneralManager | GeneralInfo | None:
        
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
        data: GeneralIntermediate | GeneralManager | GeneralInfo,
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
        data: GeneralIntermediate | GeneralManager | GeneralInfo,
    ) -> None:
        if hasattr(data, '_start_date'):
            start_date = data._start_date
        else:
            start_date = None
        
        new_end_date = datetime.now()
        if hasattr(data, '_end_date'):
            data._end_date = new_end_date

        entry, _ = cls.objects.get_or_create(
            id_string=id_string,
            start_date=start_date,
            end_date=None
        )
        entry.end_date = new_end_date
        entry.data=pickle.dumps(data)
        entry.save()


class RAMCache:
    @staticmethod
    def getCacheData(
        id_string: str,
    ) -> GeneralIntermediate | GeneralManager | GeneralInfo | None:
        return cache.get(id_string)
    
    @staticmethod
    def setCacheData(
        id_string: str,
        data: GeneralIntermediate | GeneralManager | GeneralInfo,
    ) -> None:
        if data._end_date is None or isinstance(data, GeneralInfo):
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

    def add(self, obj: object) -> None:
        id_string, _ = getIdString(obj._identification_dict)
        if id_string not in self.dependent_objects:
            self.dependent_objects[id_string].append(obj)

    def invalidate(self) -> None:
        for obj in self.dependent_objects.values():
            id_string, _ = getIdString(obj._identification_dict)
            RAMCache.invalidateCache(id_string)
            DatabaseCache.updateCacheEndDate(id_string, obj)
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
            DatabaseCache.objects.all().delete()
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not self.cache_observer_dict:
            self.__startUpCache()

    @classmethod
    def addGeneralManagerObjectToCache(
        cls,
        manager: GeneralManager
    ) -> None:
        self = cls()
        self._createCache(manager)

    @classmethod
    def addDependentObjectToCache(
        cls,
        dependency_obj_list: GeneralIntermediate | GeneralManager,
        dependent_obj: GeneralIntermediate | GeneralInfo
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
        id_string, set_cache = getIdString(identification_dict)
        data = None
        if not set_cache:
            return data
        if search_date is None:
            data = RAMCache.getCacheData(id_string)
        if data is None:
            data = DatabaseCache.getCacheData(id_string, search_date)
            if data is not None and search_date is None:
                RAMCache.setCacheData(id_string, data)
        return data

    @classmethod
    def invalidateCache(
        cls,
        object: GeneralIntermediate | GeneralManager | GeneralInfo
    ) -> None:
        self = cls()
        id_string, set_cache = getIdString(object._identification_dict)
        if set_cache:
            RAMCache.invalidateCache(id_string)
            DatabaseCache.updateCacheEndDate(id_string, object)
        if id_string in self.cache_observer_dict:
            self.cache_observer_dict[id_string].invalidate()

    @classmethod
    def removeObserver(cls, id_string: str) -> None:
        self = cls()
        del self.cache_observer_dict[id_string]

    @classmethod
    def startUpCache(cls) -> None:
        pass

    def _addDependentObjectToObserver(
        self,
        dependency_obj: GeneralIntermediate | GeneralManager,
        dependent_obj: GeneralIntermediate | GeneralInfo
    ) -> None:
        id_string, _ = getIdString(dependency_obj._identification_dict)
        if id_string not in self.cache_observer_dict:
            self.cache_observer_dict[id_string] = CacheObserver(id_string)
        self.cache_observer_dict[id_string].add(dependent_obj)

    def _createCache(
        self,
        data: GeneralIntermediate | GeneralManager | GeneralInfo
    ) -> None:
        id_string, set_cache = getIdString(data._identification_dict)
        if set_cache:
            DatabaseCache.setCacheData(id_string, data)
            RAMCache.setCacheData(id_string, data)


def updateCache(func):
    """
    Decorator function to update the cache after executing the wrapped function.
    Use this for object methods.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function with cache update functionality.
    """
    def wrapper(self, *args, **kwargs):
        CacheHandler.invalidateCache(self)
        result = func(self, *args, **kwargs)
        is_GeneralManager = isinstance(self, GeneralManager)
        is_GeneralIntermediate = isinstance(self, GeneralIntermediate)
        is_GeneralInfo = isinstance(self, GeneralInfo)
        if is_GeneralManager:
            CacheHandler.addGeneralManagerObjectToCache(self)
        elif is_GeneralIntermediate or is_GeneralInfo:
            CacheHandler.addDependentObjectToCache(self._dependencies, self)
        return result
    return wrapper


def createCache(func):
    """
    Decorator function to update the cache after executing the wrapped function.
    Use this for class methods.
    
    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function with cache update functionality.
    """
    def wrapper(cls, *args, **kwargs):
        result = func(cls, *args, **kwargs)
        is_GeneralManager = isinstance(result, GeneralManager)
        is_GeneralIntermediate = isinstance(result, GeneralIntermediate)
        is_GeneralInfo = isinstance(result, GeneralInfo)
        if is_GeneralManager:
            CacheHandler.addGeneralManagerObjectToCache(result)
            CacheHandler.invalidateCache(cls)
        elif is_GeneralIntermediate or is_GeneralInfo:
            CacheHandler.addDependentObjectToCache(result._dependencies, result)
        return result
    return wrapper


def getIdString(
        general_object: GeneralInfo | GeneralIntermediate | GeneralManager
    ) -> str:
    """
    Convert an identification_dict into a JSON string, with keys sorted. This
    wil create a unique string for each identification_dict, which can be used
    as a key in a cache.
    """
    is_managed_object = isinstance(
        general_object,
        (GeneralManager, GeneralIntermediate, GeneralInfo)
    )
    is_managed_class = (
        GeneralManager in general_object.__bases__ or
        GeneralIntermediate in general_object.__bases__ or
        GeneralInfo in general_object.__bases__
    )
        
    if is_managed_object:
        return getIdStringFromDict(general_object._identification_dict), is_managed_object
    elif is_managed_class: # is not an instance but the class itself
        return general_object.__name__, is_managed_object


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
    dependency: GeneralIntermediate | GeneralInfo
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
    if 'self' in frame.f_locals:
        instance = frame.f_locals['self']
        if isinstance(instance, (GeneralIntermediate, GeneralInfo)):
            return instance
        return recursiveSearchForIntermediateOrInfo(frame.f_back)
    return None

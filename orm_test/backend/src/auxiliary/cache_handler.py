import pickle
from backend.models import CacheIntermediate
from datetime import datetime
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from django.http import QueryDict
import json


class Watcher:
    def __init__(self, dependency: object, id_string: str) -> None:
        """
        Args:
            dependency (object): The dependency object this Watcher is
                responsible for.
        """
        self.dependency = dependency
        self.identification = id_string
        self.dependent_object_list = []

    def __repr__(self) -> None:
        return f'watcher object: {self.identification}'

    def addDependentObject(self, obj: object) -> None:
        """
        Add a dependent object to the watcher's list.

        Args:
            obj (object): The object to be added.
        """
        if obj not in self.dependent_object_list:
            self.dependent_object_list.append(obj)

    def inform(self) -> None:
        """
        Inform all dependent objects of the current time by setting their end
        dates, then destroy this watcher. This will update the end_date
        for the dependent_objects cache if it's None.
        """
        date = datetime.now()

        for obj in self.dependent_object_list:
            # obj.setCacheData(date)
            obj.expireCache(self.dependency, date)
        
        self.destroy()

    def destroy(self) -> None:
        """
        Remove this watcher from the CacheHandler.
        """
        CacheHandler.removeWatcher(self.identification)


class CacheHandler:
    """
    Singleton class responsible for managing watchers.
    """
    __instance = None
    watch_dict = {}

    def __new__(cls, *args: list, **kwargs: dict) -> object:
        """
        Create a new instance of CacheHandler if one does not already exist.
        """
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self) -> None:
        if not self.watch_dict:
            self.__startUpCacheHandler()

    @staticmethod
    def add(object: object) -> None:
        """
        Add an object to the CacheHandler.

        Args:
            object (object): The object to be added.
        """
        self = CacheHandler()
        dependencies: list = object.dependencies
        for dependency in dependencies:
            watcher_obj = self.__getOrCreateWatcher(dependency)
            watcher_obj.addDependentObject(object)
    
    @staticmethod
    def update(object: object) -> None:
        """
        Inform all dependent objects to update their cache

        Args:
            object (object): The object to be updated.
        """
        self = CacheHandler()
        watcher_obj = self.__getOrCreateWatcher(object)
        watcher_obj.inform()

    def __getOrCreateWatcher(self, dependency: object) -> Watcher:
        """
        Retrieve the watcher for a given dependency, creating one if it does not exist.

        Args:
            dependency (object): The dependency to retrieve the watcher for.
        
        Returns:
            Watcher: The watcher for the given dependency.
        """

        id_string = CacheIntermediate.getIdString(dependency._identification_dict)
        if id_string not in self.watch_dict.keys():
            self.watch_dict[id_string] = Watcher(dependency, id_string)
        
        return self.watch_dict[id_string]

    def __startUpCacheHandler(self) -> None:
        """
        Start the CacheHandler by adding all CacheIntermediate objects without end date.
        """
        to_handle = CacheIntermediate.objects.filter(end_date__isnull=True)

        for data in to_handle:
            intermediate_obj = pickle.loads(data)
            self.add(intermediate_obj)

    @staticmethod
    def removeWatcher(identification: str) -> None:
        """
        Remove a watcher from the CacheHandler based on its identification.

        Args:
            identification (str): The identification of the watcher to be removed.
        """
        self = CacheHandler()
        self.watch_dict.pop(identification, None)


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
        result = func(self, *args, **kwargs)
        self.updateCache()
        InfoCacheHandler.updateCache()
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
        cls.updateCache(result)
        InfoCacheHandler.updateCache()
        return result
    return wrapper


class InfoCacheHandler:
    """
    Singleton class responsible for managing watchers.
    """
    __instance = None
    request_url_dict = {}

    def __new__(cls, *args: list, **kwargs: dict) -> object:
        """
        Create a new instance of CacheHandler if one does not already exist.
        """
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
    
    @classmethod
    def addRequestUrl(cls, general_info_obj: object) -> None:
        """
        Add a request to the InfoCacheHandler.

        Args:
            request (object): The request to be added.
        """
        self = cls()
        self.__addRequest(general_info_obj)

    def __addRequest(self, general_info_obj: object) -> None:
        """
        Add a request to the InfoCacheHandler.

        Args:
            request (object): The request to be added.
        """

        if general_info_obj.id_string not in self.request_url_dict:
            self.request_url_dict[general_info_obj.id_string] = general_info_obj
        print(self.request_url_dict)
    
    @classmethod
    def updateCache(cls) -> None:
        """
        Inform all dependent objects to update their cache
        """
        self = cls()
        for general_info_obj in self.request_url_dict.values():
            general_info_obj._updateCache()

    @classmethod
    def startup(cls) -> None:
        """
        Start the InfoCacheHandler by adding all GeneralInfo objects.
        """
        from backend.urls import info_list

        self = cls()
        to_handle = info_list
        request = HttpRequest()
        request.method = 'GET'
        request_type = 'list'
        request.user = AnonymousUser()
        request.query_params = QueryDict(mutable=True)
        request.data = {}

        for infoClass in to_handle:
            self.addRequestUrl(infoClass(
                request=request,
                request_type= request_type
            ))
        cls.updateCache()
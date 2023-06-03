import pickle
import json
from backend.models import CacheIntermediate
from datetime import datetime

class Watcher:
    def __init__(self, dependency: object) -> None:
        """
        Args:
            dependency (object): The dependency object this Watcher is responsible for.
        """
        self.dependency = dependency
        self.identification = json.dumps(dependency.identification_dict)
        self.dependent_object_list = []

    def __repr__(self):
        return f'watcher object: {self.identification}'

    def addDependentObject(self, obj):
        """
        Add a dependent object to the watcher's list.

        Args:
            obj (object): The object to be added.
        """
        self.dependent_object_list.append(obj)

    def inform(self):
        """
        Inform all dependent objects of the current time by setting their end dates, then destroy this watcher.
        This will update the end_date for the dependent_objects cache.
        """
        date = datetime.now()

        for obj in self.dependent_object_list:
            obj.setEndDate(date)
        
        self.destroy()

    def destroy(self):
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

    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of CacheHandler if one does not already exist.
        """
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        if not self.watch_dict:
            self.__startUpCacheHandler()

    @staticmethod
    def add(object):
        """
        Add an object to the CacheHandler.

        Args:
            object (object): The object to be added.
        """
        self = CacheHandler()
        dependencies = object.dependencies
        for dependency in dependencies:
            watcher_obj = self.__getOrCreateWatcher(dependency)
            watcher_obj.addDependentObject(object)
    
    @staticmethod
    def update(object):
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

        identification = json.dumps(dependency.identification_dict)
        if identification not in self.watch_dict.keys():
            self.watch_dict[identification] = Watcher(dependency)
        
        return self.watch_dict[identification]

    @classmethod
    def __startUpCacheHandler(cls) -> None:
        """
        Start the CacheHandler by adding all CacheIntermediate objects without end date.
        """
        cache_handler_obj = cls()
        to_handle = CacheIntermediate.objects.filter(end_date__isnull=True)

        for data in to_handle:
            intermediate_obj = pickle.loads(data)
            cache_handler_obj.add(intermediate_obj)

    @staticmethod
    def removeWatcher(identification: str) -> None:
        self = CacheHandler()
        self.watch_dict.pop(identification, None)

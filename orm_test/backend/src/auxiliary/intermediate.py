import inspect
from backend.models import CacheIntermediate
from django.core.cache import cache
from datetime import datetime
from backend.src.auxiliary.exceptions import MissingAttributeError

class GeneralIntermediate:

    def __new__(cls, *args: list, **kwargs: dict) -> object:
        # Get the names of the arguments in __init__
        init_params = inspect.signature(cls.__init__).parameters
        
        # Map the positional arguments to their names
        kwargs.update(dict(zip(init_params, args)))

        search_date = kwargs.pop('search_date', None)
        use_cache = kwargs.pop('use_cache', None)

        identification_dict = kwargs
        intermediate_name = cls.__name__

        if use_cache:
            cached_instance = CacheIntermediate.get_cache_data(
                intermediate_name=intermediate_name,
                identification_dict=identification_dict,
                date=search_date
            )
            if cached_instance:
                return cached_instance

        instance = super().__new__(cls)
        instance.__init__({**kwargs, 'search_date': search_date})
        instance.identification_dict = identification_dict
        return instance

    def __init__(self, search_date: datetime | None, **kwargs: dict) -> None:
        self.identification_dict: dict
        self.dependencies: list
        self.search_date = search_date
        self.__checkIfDependenciesAreFilled()
        
        self.start_date = self.__getStartDate()
        self.end_date = self.__getEndDate()

    def __eq__(self, other: object) -> bool:
        own_id_string = CacheIntermediate.getIdString(self.identification_dict)
        other_id_string = CacheIntermediate.getIdString(self.other)
        return (
            isinstance(other, self.__class__) and
            own_id_string == other_id_string
        )
    
    def __getStartDate(self) -> datetime:
        start_date_list = [
            dependency.start_date for dependency in self.dependencies
            if dependency.start_date is not None
        ]
        return min(start_date_list)
        
    def __getEndDate(self) -> datetime:
        end_date_list = [
            dependency.start_date for dependency in self.dependencies
            if dependency.start_date is not None
        ]
        if len(end_date_list) == 0:
            return None
        return min(end_date_list)
    
    def __checkIfDependenciesAreFilled(self):
        if not hasattr(self, 'dependencies'):
            raise MissingAttributeError(
                '''
                Every intermediate class needs to have a dependencies attribute
                to work properly! It needs to contain a list of all necessary
                intermediate and manager objects.
                '''
            )
        if type(self.dependencies) != list:
            raise TypeError(
                'The attribute "dependencies" needs to be of type list'
            )
        if len(self.dependencies) == 0:
            raise ValueError(
                '''
                The attribute "dependencies" needs to contain all necessary
                intermediate and manager objects. Intermediate without
                dependencies is not possible.
                '''
            )
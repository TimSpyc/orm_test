import inspect
from backend.models import CacheIntermediate
from django.core.cache import cache
import json

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

    def __init__(self, search_date: int | None, **kwargs: dict) -> None:
        self.identification_dict = None
        self.search_date = search_date

        self.start_date = 
        self.end_date =

    def __eq__(self, other: object) -> bool:
        own_id_string = CacheIntermediate.getIdString(self.identification_dict)
        other_id_string = CacheIntermediate.getIdString(self.other)
        return (
            isinstance(other, self.__class__) and
            own_id_string == other_id_string
        )
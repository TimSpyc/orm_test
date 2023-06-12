import inspect
from backend.models import CacheIntermediate
from datetime import datetime
from backend.src.auxiliary.exceptions import MissingAttributeError
from backend.src.auxiliary.scenario_handler import ScenarioHandler
from backend.src.auxiliary.cache_handler import CacheHandler
from backend.src.auxiliary.manager import GeneralManager

class GeneralIntermediate:
    """
    A general class representing an intermediate data object, which stores
    its dependencies and their respective start and end dates.

    The class uses caching to retrieve and store instances, and provides
    methods for comparing instances and verifying their dependencies.
    """
    relevant_scenario_keys: list
    
    def __new__(cls, *args: list, **kwargs: dict) -> object:
        """
        Overload the __new__ method to allow for cache retrieval of instances.

        Args:
            args (list): The positional arguments for the __init__ method.
            kwargs (dict): The keyword arguments for the __init__ method.

        Returns:
            object: An instance of the class, either retrieved from cache or
            newly created.
        """
        if kwargs == {} and args == []:
            return super().__new__(cls)

        kwargs = cls.__makeArgsToKwargs(args, kwargs)

        search_date = kwargs.pop('search_date', None)
        use_cache = kwargs.pop('use_cache', None)
        scenario_dict = kwargs.pop('scenario_dict', {})

        rel_scenario, _ = cls.__cleanScenarioDict(scenario_dict)

        kwargs['relevant_scenarios'] = rel_scenario
        intermediate_name = cls.__name__

        if use_cache:
            cached_instance = CacheIntermediate.get_cache_data(
                intermediate_name=intermediate_name,
                identification_dict=kwargs,
                date=search_date
            )
            if cached_instance:
                return cached_instance

        instance = super().__new__(cls)
        instance.__init__({**kwargs, 'search_date': search_date})
        instance.identification_dict = kwargs

        return instance

    def __init__(
        self,
        search_date: datetime | None,
        scenario_dict: dict,
        dependencies: list
    ) -> None:
        """
        Initialize an instance of the class with the given search date and
        keyword arguments.

        Args:
            search_date (datetime | None): The date to use when searching
                the cache.
            kwargs (dict): Additional keyword arguments to use when
                initializing the instance.
        """
        self.identification_dict: dict
        self.scenario_handler : ScenarioHandler(scenario_dict)
        self.dependencies = dependencies
        self.search_date = search_date
        self.__checkIfDependenciesAreFilled()
        
        self.start_date = self.__getStartDate()
        self.end_date = self.__getEndDate()
        CacheHandler.add(self)

    def __eq__(self, other: object) -> bool:
        """
        Overload the __eq__ method to allow for comparing instances based
        on their identification string.

        Args:
            other (object): The other object to compare with.

        Returns:
            bool: True if the two instances have the same identification
                string, False otherwise.
        """
        if not isinstance(other, GeneralIntermediate):
            return False

        own_id_string = CacheIntermediate.getIdString(
            self.identification_dict
        )
        other_id_string = CacheIntermediate.getIdString(
            other.identification_dict
        )
        
        return (
            isinstance(other, self.__class__) and
            own_id_string == other_id_string
        )
    
    def __getStartDate(self) -> datetime:
        """
        Get the earliest start date among the dependencies of the instance.

        Returns:
            datetime: The earliest start date.
        """
        start_date_list = [
            dependency.start_date for dependency in self.dependencies
            if dependency.start_date is not None
        ]
        return min(start_date_list)
        
    def __getEndDate(self) -> datetime | None:
        """
        Get the earliest end date among the dependencies of the instance.

        Returns:
            datetime: The earliest end date, or None if no end dates are
                present.
        """
        end_date_list = [
            dependency.end_date for dependency in self.dependencies
            if dependency.end_date is not None
        ]
        if len(end_date_list) == 0:
            return None
        return min(end_date_list)
    
    def __checkIfDependenciesAreFilled(self):
        """
        Check if the dependencies of the instance are properly set.

        Raises:
            MissingAttributeError: If the dependencies attribute is not set.
            TypeError: If the dependencies attribute is not of type list.
            ValueError: If the dependencies attribute is empty.
        """
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
                f'''
                The attribute "dependencies" needs to be of type list not
                {type(self.dependencies)}
                '''
            )
        if len(self.dependencies) == 0:
            raise ValueError(
                '''
                The attribute "dependencies" needs to contain all necessary
                intermediate and manager objects. An intermediate without
                dependencies is not possible.
                '''
            )
        for dependency in self.dependencies:
            if (
                not isinstance(dependency, GeneralIntermediate) or 
                not isinstance(dependency, GeneralManager)
            ):
                raise TypeError(
                    f'''
                    All list items of "dependencies" need to be of type 
                    GeneralIntermediate or GeneralManager not of type 
                    {type(dependency)}
                    '''
                )
    
    @classmethod
    def __makeArgsToKwargs(cls, args: list, kwargs: dict) -> dict:
        """
        This method takes the arguments and keywords arguments of the class
        constructor, maps the positional arguments to their respective
        parameter names, and returns a dictionary that represents all arguments
        as keyword arguments.

        Args:
            args (list): The positional arguments provided to the class
                constructor.
            kwargs (dict): The keyword arguments provided to the class
                constructor.

        Returns:
            dict: A dictionary containing all arguments as keyword arguments.
        """
        extended_kwargs = {**kwargs}
        # Get the names of the arguments in __init__
        init_params = inspect.signature(cls.__init__).parameters
        
        # Map the positional arguments to their names
        extended_kwargs.update(dict(zip(init_params, args)))
        
        return extended_kwargs

    @classmethod
    def __cleanScenarioDict(
        cls,
        scenario_dict: dict
    ) -> tuple[dict, ScenarioHandler]:
        """
        This method takes a scenario dictionary, uses a ScenarioHandler to
        extract the relevant scenarios (defined by cls.relevant_scenario_keys),
        and returns both the relevant scenarios and the ScenarioHandler
        instance.

        Args:
            scenario_dict (dict): The scenario dictionary to be cleaned.

        Returns:
            tuple(dict, ScenarioHandler): A tuple containing the cleaned
                scenario dictionary and the ScenarioHandler instance used for
                the cleaning.
        """

        scenario_handler = ScenarioHandler(scenario_dict)
        relevant_scenarios = scenario_handler.\
            getRelevantScenarioDict(cls.relevant_scenario_keys)

        return relevant_scenarios, scenario_handler

    def updateCache(self):
        CacheIntermediate.set_cache_data(
            intermediate_name=self.__class__.__name__,
            identification_dict=self.identification_dict,
            data=self,
            start_date=self.start_date,
            end_date=self.end_date
        )

    def setEndDate(self, end_date: datetime):
        if self.end_date is None:
            self.end_date = end_date
            self.updateCache()
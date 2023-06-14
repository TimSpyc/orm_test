from backend import models
from backend.src.auxiliary.exceptions import NonExistentGroupError, NotUpdatableError, NotValidIdError
import re
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from backend.models import CacheManager, User
from datetime import datetime
from django.db.models import Max, Model
from django.db.models.query import QuerySet
import timeit
from django.db import models


def timing(func):
    """
    A Python decorator that measures the execution time of a function and prints it.

    Args:
        func: The function whose execution time is to be measured.

    Returns:
        A new function that wraps the passed function and measures its execution time.

    Example:
        @timing
        def my_function():
            # Code for your function goes here
            pass

    The `timing` function measures the execution time of the passed function and prints it in seconds.
    """
    def wrapper(*args, **kwargs):
        execution_time = timeit.timeit(lambda: func(*args, **kwargs), number=1)
        print(
         f"The function {func.__name__} was run in {execution_time} seconds.")
    return wrapper

def transferToSnakeCase(name):
    """
    Convert a string from CamelCase to snake_case.

    Args:
        name (str): The input string in CamelCase.

    Returns:
        str: The output string in snake_case.
    """
    return re.sub(
        r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '_', name).lower()

def noneValueInNotNullField(not_null_fields, data_dict):
    """
    Check if there is any None value in the fields marked as NOT NULL.

    Args:
        not_null_fields (list): A list of fields that are marked as NOT NULL.
        data_dict (dict): A dictionary containing field keys and their respective values.

    Returns:
        bool: True if any None value is found in the NOT NULL fields, False otherwise.
    """
    data_is_none_list = []
    for key, data in data_dict.items():
        if data is None:
            data_is_none_list.append(key)
    
    return bool(set(not_null_fields).intersection(set(data_is_none_list)))

def updateCache(func):
    """
    Decorator function to update the cache after executing the wrapped function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function with cache update functionality.
    """
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.updateCache()

        return result
    return wrapper

def createCache(func):
    """
    Decorator function to update the cache after executing the wrapped function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function with cache update functionality.
    """
    def wrapper(cls, *args, **kwargs):
        result = func(cls, *args, **kwargs)
        cls.updateCache(result)

        return result
    return wrapper


class GeneralManager:
    """
    GeneralManager is a base class for managing objects with a group model and a data model.
    It provides caching capabilities and initialization logic for derived classes.

    Attributes:
        group_model (Model): The group model class associated with this manager.
        data_model (Model): The data model class associated with this manager.
    """
    group_model: Model
    data_model: Model

    def __new__(cls,group_id=None, search_date=None, use_cache=True, **kwargs):
        """
        Create a new instance of the Manager or 
        return a cached instance if available.

        Args:
            group_id (int, optional): The ID of the group object. 
                Defaults to None for caching only.
            search_date (datetime, optional): The date for which to 
                search the data object. Defaults to None (latest data).
            use_cache (bool, optional): Whether to use the cache when 
                searching for instances. Defaults to True.

        Returns:
            manager: A new or cached instance of the manager.
        """

        manager_name = cls.__name__

        if hasattr(cls, 'group_model'):
            group_table_id_name = f'''
                {transferToSnakeCase(cls.group_model.__name__)}_id
            '''
            if group_table_id_name in kwargs:
                group_id = kwargs[group_table_id_name]
        
        if group_id is None:
            return super().__new__(cls)
        if use_cache:
            group_model_name = transferToSnakeCase(cls.group_model.__name__)
            group_model_obj = cls.group_model(group_id)

            if search_date is None:
                cached_instance = cache.get(f"{manager_name}|{group_id}")
                if cached_instance is not None:
                    return cached_instance
            cached_instance = CacheManager.get_cache_data(
                manager_name, 
                group_model_obj, 
                group_model_name, 
                cls.data_model, 
                group_id, 
                search_date
                )
            if cached_instance:
                cls.updateCache(cached_instance)
                return cached_instance

        instance = super().__new__(cls)
        instance.__init__(group_id, search_date)
        if use_cache:
            cls.updateCache(instance)
        return instance

    def __init__(self, group_id: int, search_date=None):
        """
        Initialize the manager with the given group_id and date.
        And save all default attributes.

        Args:
            group_id (int): The ID of the group object.
            search_date (datetime, optional): The date for which to search
                the data object. Defaults to None (latest data).
        """
        self.__group_model_name = self.__getGroupModelName()
        group_obj = self.__getGroupObject(group_id)
        data_obj = self.__getDataObject(group_obj, search_date)

        self.__group_obj = group_obj
        self.__data_obj = data_obj

        self.id = data_obj.id
        self.group_id = group_obj.id
        self.creator_id = data_obj.creator.id
        self.creator = data_obj.creator
        self.active = data_obj.active
        self.start_date = data_obj.date
        self.end_date = self.__getEndDate()


        self.search_date = search_date

        return group_obj, data_obj

    def __eq__(self,other):
        return (
            isinstance(other, self.__class__) and
            self.group_id == other.group_id and
            self.start_date == other.start_date
        )

    @classmethod
    def __getGroupModelName(cls):
        """
        Get group model name. Raises value error if group model name 
        is not in data model columns!
        Returns:
            group_model_name
        """
        column_list = cls.__getColumnList(cls.data_model)
        group_model_name = transferToSnakeCase(cls.group_model.__name__)
        db_column_exists, *_ = cls.\
        __searchForColumn(group_model_name, column_list)
        
        if not db_column_exists:
            raise ValueError (
                f'''the column {group_model_name} does not exist 
                in your data model ({cls.data_model})!''')
        
        return group_model_name

    @classmethod
    def all(cls, search_date=None) -> list:
        """
        Retrieves all objects of the manager's class, 
        optionally filtering by search_date.

        Args:
            search_date (datetime.date, optional): A date to filter 
                the objects by. If specified, only objects with a date 
                less than or equal to the search_date will be included.

        Returns:
            list: A list of manager objects, 
                filtered by the optional search_date if provided.
        """
        return cls.filter(search_date=search_date)

    @classmethod
    def filter(cls, search_date=None, **kwargs: any) -> list:
        """Creates a list of objects based on the given parameters.

        Keyword arguments:
        search_date (datetime.date, optional) -- An optional argument 
            that specifies the search date for the objects to be created.
        **kwargs: A variable that contains key-value pairs of filter conditions
            for the database query.

        Returns:
        list -- A list of manager objects that match the filter conditions.

        Example:
        To create a list of all manager objects where the 'name' column 
        is equal to 'foo': filter(name='foo')
        """
        if search_date is None:
            search_date = datetime.now()

        group_model_column_list = cls.__getColumnList(cls.group_model)
        data_model_column_list = cls.__getColumnList(cls.data_model)

        group_data_dict, data_data_dict = cls.\
            __getDataForGroupAndDataTableByKwargs(
            data_model_column_list,
            group_model_column_list, 
            **kwargs
            )
        found_group_id_date_combination_dict_list = cls.\
            __getFilteredManagerList(
            data_data_dict,
            group_data_dict, 
            search_date
            )
        return cls.__createManagerObjectsFromDictList(
            found_group_id_date_combination_dict_list
            )

    @classmethod
    def __getDataForGroupAndDataTableByKwargs(
        cls, 
        data_model_column_list: list, 
        group_model_column_list: list, 
        **kwargs: any
    ) -> tuple[dict,dict]:
        """
        Separate the input data into group and data dictionaries 
        based on the provided column lists.

        Args:
            data_model_column_list (list): 
                A list of available column names in the data model.
            group_model_column_list (list): 
                A list of available column names in the group model.
            **kwargs: 
                A dictionary of key-value pairs to be searched in the models.

        Returns:
            tuple: A tuple containing:
                - dict: A dictionary containing group model data.
                - dict: A dictionary containing data model data.

        Raises:
            ValueError: 
                If the database column is not unique or 
                has no corresponding column in the models.
        """
        not_unique_column_names = [
            column_name for column_name in group_model_column_list
            if column_name in data_model_column_list
        ]
        
        group_data_dict = {}
        data_data_dict = {}
        for _db_column, _value in kwargs.items():
            db_column = _db_column
            value = _value
            if _db_column in not_unique_column_names:
                raise ValueError(
                    f'''
                        It's not possible to search for {_db_column} because
                        the value exists in group and data model.
                    '''
                )
            is_in_group_model,db_column,value=cls.__getValueAndColumnIfExists(
                db_column, 
                group_model_column_list, 
                cls.group_model, value
                )
            is_in_data_model,db_column,value=cls.__getValueAndColumnIfExists(
                db_column, 
                data_model_column_list, 
                cls.data_model, 
                value
                )

            if not is_in_group_model and not is_in_data_model:
                raise ValueError(
                    f'''
                     You can't search/create data that is not available in DB.
                     {db_column} has no corresponding db column.
                    '''
                )

            elif is_in_group_model:
                group_data_dict[db_column] = value
            elif is_in_data_model:
                data_data_dict[db_column] = value
        
        return group_data_dict, data_data_dict

    @classmethod
    def __getFilteredManagerList(
        cls, 
        data_search_dict: dict, 
        group_search_dict: dict, 
        search_date: datetime
    ) -> list:
        """
        Get a filtered list of manager instances based 
        on the provided search criteria.

        Args:
            data_search_dict (dict): 
                A dictionary containing data model search criteria.
            group_search_dict (dict): 
                A dictionary containing group model search criteria.
            search_date (datetime): 
                The date to be used for filtering. Defaults to None.

        Returns:
            list: A list of filtered manager instances.
        """

        group_model_name = cls.__getGroupModelName()
        data_table_name = cls.data_model._meta.db_table

        newest_data_table_entries = cls.data_model.objects.raw(f'''
            SELECT
                id
            FROM
                {data_table_name}
            WHERE
                ({group_model_name}_id, date) in (
                    SELECT
                        {group_model_name}_id, max(date)
                    FROM
                        {data_table_name}
                    WHERE
                        date <= '{search_date}'
                    GROUP BY
                        {group_model_name}_id
                )
        ''')
        group_model_ids = cls.data_model.objects.filter(
            **{**data_search_dict, 
            'id__in': [data_obj.id for data_obj in newest_data_table_entries]}
            ).values(f'{group_model_name}_id')
        
        group_id_list = cls.group_model.objects.filter(
            **{**group_search_dict, 'id__in': group_model_ids}
            ).values_list('id', flat=True)
        
        return [{f'{group_model_name}_id': group_id,
                  'search_date': search_date} for group_id in group_id_list]

    @classmethod
    def __createManagerObjectsFromDictList(
        cls, 
        creation_dict_list: list
    ) -> list:
        """
        Creates a list of manager objects from a list of dictionaries.

        Args:
            creation_dict_list (list): 
                A list of dictionaries representing the data 
                for manager object creation.

        Returns:
            list: 
                A list of manager objects created 
                from the provided dictionary data.
        """
        return [cls(**data) for data in creation_dict_list] 

    def __errorIfNotUpdatable(self) -> None:
        """
        Raise an error if the current instance is not updatable.

        Raises:
            NotUpdatableError: 
                If the current instance is not the latest data in the database.
        """
        latest_db_id = self.data_model.objects.filter(
            **{transferToSnakeCase(
            self.group_model.__name__): self.__group_obj}
            ).values('id').latest('date')['id']

        is_latest = self.id == latest_db_id
        if not is_latest:
            raise NotUpdatableError(
                f"""
                You can only update the latest data, this is not the latest
                data. Latest id = {latest_db_id}, your id = {self.id}
                """
            )

    @staticmethod
    def __searchForColumn(
        column_name: str, 
        column_list: list
    ) -> tuple[bool,str,bool,bool]:
        """
        Search for a given column name in the provided column list and 
        determine if it references a model or many-to-many relationship.

        Args:
            column_name (str): The name of the column to search for.
            column_list (list): A list of available column names.

        Returns:
            tuple: A tuple containing:
                - bool: Whether the column exists in the column list.
                - str: The updated column name if it references a model or 
                    many-to-many relationship or the original column name.
                - bool: Whether the column references a model.
                - bool: Whether the column references a many-to-many relationship.
        """
        db_column_exists = False

        column_name, is_reverencing_model = GeneralManager.\
            __checkIfColumnReferencesModel(
            column_name, 
            column_list
            )
        column_name, is_many_to_many = GeneralManager.\
            __checkIfColumnReferencesManyToMany(
            column_name, 
            column_list
            )

        if column_name in column_list:
            db_column_exists = True

        return db_column_exists, column_name, \
               is_reverencing_model, is_many_to_many

    @staticmethod
    def __checkIfColumnReferenceBaseExists(
        column_name: str, 
        available_column_list: list, 
        string_to_compare: str
    ) ->tuple[str, bool]:
        """
        Check if the given column name references a model in the provided 
        column list. Reference relationship columns must end with 
        '_id' or '_id_list.

        Args:
            column_name (str): The name of the column to check.
            available_column_list (list): A list of available column names.
            string_to_compare (str) : 
                The string to compare with the column name ending.

        Returns:
             Tuple: 
                The modified column name and a boolean if is_referencing_model.
        """
        negative_length_to_cut = - len(string_to_compare)
        db_column_contains_string_to_compare = string_to_compare \
        == column_name[negative_length_to_cut:]
        is_reverencing_model = False
        
        if db_column_contains_string_to_compare:
            db_column_model_name = column_name[:negative_length_to_cut]
            if db_column_model_name in available_column_list:
                column_name = db_column_model_name
                is_reverencing_model = True
        
        return column_name, is_reverencing_model

    @staticmethod
    def __checkIfColumnReferencesManyToMany(
        column_name: str, 
        available_column_list: list
    ) -> tuple[str,bool]:
        """
        Check if the given column name references a many-to-many relationship
        in the provided column list. Many-to-many relationship columns 
        must end with '_id_list'.

        Args:
            column_name (str): The name of the column to check.
            available_column_list (list): A list of available column names.

        Returns:
            Tuple: 
                The modified column name and a boolean if is_referencing_model.
        """
        return  GeneralManager.__checkIfColumnReferenceBaseExists(
            column_name, 
            available_column_list, "_id_list")

    @staticmethod
    def __checkIfColumnReferencesModel(
        column_name: str, 
        available_column_list: list
    ) -> tuple[str,bool]:
        """
        Check if the given column name references a model in the provided 
        column list. Reference relationship columns must end with '_id'

        Args:
            column_name (str): The name of the column to check.
            available_column_list (list): A list of available column names.

        Returns:
            Tuple: 
                The modified column name and a boolean if is_referencing_model.
        """        
        return  GeneralManager.__checkIfColumnReferenceBaseExists(
            column_name, 
            available_column_list, "_id")

    @staticmethod
    def __getValueForReverencedModelById(
        current_model: models.Model, 
        db_column: str, id: int
    ) -> models.Model:
        """
        Retrieve the value of a referenced model by its ID.

        Args:
            current_model (Model): The current Django model.
            db_column (str): The name of the database column.
            id (int): The ID of the referenced model.

        Returns:
            Model: The referenced model object.

        Raises:
        NotValidIdError: If ID does not exist in the database.
        """
        model_for_db_value = (
            current_model._meta.get_field(db_column)
            .remote_field.model
        )
        model_obj = (
            model_for_db_value.objects.filter(id=id).first()
        )
        if model_obj is None:
            raise NotValidIdError
        (f"{model_for_db_value} with id {id} does not exist.")
        return model_obj

    @staticmethod
    def __getValueForManyToManyByIdList(
        current_model: models.Model, 
        db_column: str, 
        id_list: list | set | tuple
    ) -> models.QuerySet:
        """
        Retrieve a list of values for a many-to-many 
        relationship by a list of IDs.

        Args:
            current_model (Model): The current Django model.
            db_column (str): The name of the database column.
            id_list (list|set|tuple): 
                A list of IDs for the many-to-many relationship.

        Returns:
            QuerySet: A queryset of related model objects.
        
        Raises:
        NotValidIdError: 
            If one or more IDs in the list do not exist in the database.
        """
        id_set = set(id_list)
        model_for_db_value = (
            current_model._meta.get_field(db_column)
            .remote_field.model
        )
        existing_ids = model_for_db_value.objects.filter(
            id__in = id_set
            ).values_list('id', flat=True)
        not_existing_ids = id_set - set(existing_ids)       
        if not_existing_ids:
             raise NotValidIdError(
                 f'''One or more IDs in the list do not exist 
                 in the database: {not_existing_ids}''')                                                           
        
        model_obj_list = (                                                                   
            model_for_db_value.objects.filter(id__in=id_set)
        )
        return model_obj_list

    @staticmethod
    def __getValueAndColumnIfExists(
        db_column: str,
        model_column_list: list,
        model: models.Model,
        value: any
    ) -> tuple[bool, str, any]:
        """
        Check if a column exists in the model column list and retrieve its
        value.

        Args:
            db_column (str): The name of the database column.
            model_column_list (list): A list of available column names in the
                model.
            model (Model): The Django model.
            value (any): The value associated with the database column.

        Returns:
            tuple: A tuple containing:
                - bool: Whether the column exists in the model column list.
                - str: The updated column name.
                - value: The value associated with the database column.
        """
        is_in_model, db_column, is_reverencing_model, is_many_to_many = \
            GeneralManager.__searchForColumn(
                db_column,
                model_column_list
            )
        if is_reverencing_model:
            value = GeneralManager.__getValueForReverencedModelById(
                model,
                db_column,
                id = value
            )
        if is_many_to_many:
            value = GeneralManager.__getValueForManyToManyByIdList(
                model,
                db_column,
                id_list = value
            ) 
        
        return is_in_model, db_column, value

    @staticmethod
    def __checkInputDictForInvalidKeys(
        manager_object: object, 
        column_list: list, 
        invalid_key_list: list
    ) -> None:
        """
        Checks if the given column_list contains invalid keys that should 
        not be overridden.

        Args:
            manager_object (object): 
                The manager object to which the keys belong.
            column_list (list): List of column names to be checked.
            invalid_key_list (list): 
                List of invalid keys that should not be overridden.

        Raises:
            ValueError: 
                If any of the keys in the column_list is found in 
                the invalid_key_list.
        """
        for db_column in column_list:
            if db_column in invalid_key_list:
                raise ValueError(
                    f'''
                        You can't override date and
                        {manager_object.__group_model_name}_id by yourself.
                        Date is always the current date and
                        {manager_object.__group_model_name}_id is unchangeable
                        unless you create a new instance with .create(). The
                        creator_user_id is an extra kwarg because its
                        mandatory and not allowed here.
                    '''
                )
            

    def __getToCheckListForUpdate(self) -> list:
        """
        Returns:
            list: List of keys to be checked for update.
        """
        return [
                'date',
                self.__group_model_name,
                'creator_user_id'
            ]
    
    def __getToCheckListForCreation() -> list:
        """
        Returns:
        list: List of keys to be checked for creation.
        """
        return [
                'date',
                'creator_user_id'
            ]

    @staticmethod
    def __getColumnList(model: models.Model) -> list:
        """
        Retrieve a list of column names for the given model.

        Args:
            model (Model): The Django model.

        Returns:
            list: A list of column names for the model.
        """
        column_list = [field.name for field in model._meta.get_fields()]
        return column_list

    @updateCache
    def update(self, creator_user_id: int, **kwargs: any):
        """
        Update the current instance with new data, 
        uploads to db and refresh the cache.

        Args:
            creator_user_id (int): The ID of the user who is making the update.
            **kwargs: Key-value pairs representing the new data to be updated.
        """
        self.__errorIfNotUpdatable()
        data_model_column_list = self.__getColumnList(self.data_model)
        group_model_column_list = [] #Unchangeable by update
        self.__checkInputDictForInvalidKeys(
            manager_object = self,
            column_list = kwargs.keys(),
            invalid_key_list = self.__getToCheckListForUpdate()
        )

        _, data_data_dict = self.__getDataForGroupAndDataTableByKwargs(
            data_model_column_list, 
            group_model_column_list, 
            **kwargs
            )

        group_model_name = transferToSnakeCase(self.group_model.__name__)
        group_model_obj = self.__getGroupObject(self.group_id)

        latest_data = self.data_model.objects.filter(
            **{group_model_name: group_model_obj}
            ).values().latest('date')
        if latest_data == []:
            latest_data = {}

        self.__writeDataData(
            latest_data, 
            data_data_dict, 
            creator_user_id, 
            self.__group_obj)
        self.__init__(self.group_id)
        
    @classmethod
    def __writeDataData(
        cls, 
        latest_data: dict, 
        data_data_dict: dict, 
        creator_user_id: int, 
        group_obj: models.Model
    ) -> None:
        """
        Write new data to the data model.

        Args:
            latest_data (dict): The latest data fetched from the data model.
            data_data_dict (dict): 
                Dictionary containing the new data to be updated.
            creator_user_id (int): The ID of the user who is making the update.
            group_obj (GroupModel): 
                The group model instance to which the data belongs.
        """
        group_table_name = transferToSnakeCase(group_obj.__class__.__name__)
        
        new_data = {
            **latest_data,
            **data_data_dict,
            **{
                'date': datetime.now(),
                'creator':User.objects.get(id=creator_user_id),
                group_table_name: group_obj
            }
        }
        try:
            del new_data['id']
        except KeyError:
            pass

        many_to_many_dict = {}
        not_many_to_many_dict = {}
        
        for key, value in new_data.items():
            if type(value) == QuerySet:
                many_to_many_dict[key] = value
            else:
                not_many_to_many_dict[key] = value

        new_data_in_model = cls.data_model(
            **not_many_to_many_dict
        )
        new_data_in_model.save()

        for key, value_list in many_to_many_dict.items():
            for value in value_list:
                getattr(new_data_in_model, key).add(value)
        
        new_data_in_model.save()

    def deactivate(self, creator_user_id: int) -> None:
        """
        Deactivate the current instance and set active=False in db.

        Args:
            creator_user_id (int): 
                The ID of the user who is deactivating the instance.
        """
        if not self.active:
            raise NotUpdatableError('This manager is already deactivated')

        self.update(creator_user_id, active=False)
    
    @classmethod
    def __isDataUploadable(
        cls, 
        data_dict: dict, 
        model: models.Model
    ) -> tuple[bool,bool,bool]:
        """
        Check if the data provided in the dictionary can be uploaded to 
        the specified model.

        Args:
            data_dict (dict): A dictionary containing the data to be uploaded.
            model (Model): 
                The Django model to which the data should be uploaded.

        Returns:
            tuple: A tuple of three boolean values, each indicating the 
                fulfillment of the following criteria:
                1. Whether all unique fields are present in the data_dict.
                2. Whether all not_null fields are present in the data_dict.
                3. Whether all not_null fields in the data_dict contain data 
                    (no None values).
        """
        unique_fields = []
        for unique_field_tuple in model._meta.unique_together:
            unique_fields = [*unique_field_tuple, *unique_fields]
        not_null_fields = [field.name for field in model._meta.get_fields() 
                           if not field.null and not field.auto_created]
        
        data_dict_extended_list = list(data_dict.keys())
        data_dict_extended_list.extend(
            ['date', 
             'creator', 
             'active', 
             transferToSnakeCase(cls.group_model.__name__)])
        
        contains_all_unique_fields = set(
            unique_fields).issubset(set(data_dict_extended_list))
        contains_all_not_null_fields = set(
            not_null_fields).issubset(set(data_dict_extended_list))
        all_not_null_fields_contain_data = not noneValueInNotNullField(
            not_null_fields, 
            data_dict
            )

        return (
            contains_all_unique_fields,
            contains_all_not_null_fields,
            all_not_null_fields_contain_data
        )

    @classmethod
    @createCache
    def create(cls, creator_user_id: int, **kwargs: any) -> object:
        """
        Create a new instance of the current class and initialize cache.

        Args:
            creator_user_id (int): 
                The ID of the user who is creating the new instance.
            **kwargs: Key-value pairs representing the data to be used for 
                creating the new instance.

        Returns:
            cls: A new instance of the current manager class.
        """
        data_model_column_list = cls.__getColumnList(cls.data_model)
        group_model_column_list = cls.__getColumnList(cls.group_model)
        cls.__checkInputDictForInvalidKeys(
            manager_object = cls,
            column_list = kwargs.keys(),
            invalid_key_list = cls.__getToCheckListForCreation()
        )
        group_data_dict, data_data_dict=cls.\
        __getDataForGroupAndDataTableByKwargs(
            data_model_column_list, 
            group_model_column_list, 
            **kwargs)

        unique_fields = cls.group_model._meta.unique_together

        is_group_data_uploadable = all(
            cls.__isDataUploadable(group_data_dict, cls.group_model))
        is_data_data_uploadable = all(
            cls.__isDataUploadable(data_data_dict, cls.data_model))

        if is_group_data_uploadable and is_data_data_uploadable:

            if len(unique_fields) == 0:
                new_group_obj = cls.group_model(
                    **group_data_dict
                )
            else:
                new_group_obj, _ = cls.group_model.objects.get_or_create(
                    **group_data_dict
                )
            new_group_obj.save()

            cls.__writeDataData(
                {}, 
                data_data_dict, 
                creator_user_id, 
                new_group_obj)

            return cls(new_group_obj.id)

        else:
            is_group_data_uploadable = cls.__isDataUploadable(
                                       group_data_dict, 
                                       cls.group_model)
            is_data_data_uploadable = cls.__isDataUploadable(
                                      data_data_dict, 
                                      cls.data_model)
        raise ValueError(
            f'''
            The given **kwargs are not sufficient.
            Because group table data:
                contains_all_unique_fields: {is_group_data_uploadable[0]}
                contains_all_not_null_fields: {is_group_data_uploadable[1]}
                all_not_null_fields_contain_data: {is_group_data_uploadable[2]}
            Because data table data:
                contains_all_unique_fields: {is_data_data_uploadable[0]}
                contains_all_not_null_fields: {is_data_data_uploadable[1]}
                all_not_null_fields_contain_data: {is_data_data_uploadable[2]}
            '''
        )

    def __getGroupObject(self, group_id: int) -> models.Model:
        """
        Get the group model instance with the provided group ID.

        Args:
            group_id (int): The ID of the group model instance to be fetched.

        Returns:
            GroupModel: The group model instance with the provided ID.
        """
        try:
            return self.group_model.objects.get(id=group_id)
        except ObjectDoesNotExist:
            raise NotUpdatableError(
                f'''{self.group_model.__name__} with 
                    id {group_id} does not exist'''
            )
    
    def __getDataObject(
        self, 
        group_obj: models.Model, 
        search_date: datetime
    ) -> models.Model:
        """
        Get the data model instance for the given group object and date.

        Args:
            group_obj (GroupModel): 
                The group model instance for which the data is to be fetched.
            search_date (datetime):     
                The date for which the data is to be fetched.

        Returns:
            DataModel: 
                The data model instance for the given group object and date.
        """
        try:
            if search_date is None:
                data_obj = self.data_model.objects.filter(
                    **{self.__group_model_name: group_obj}
                ).latest('date')
            else:
                data_obj = self.data_model.objects.filter(
                    **{self.__group_model_name: group_obj,
                    'date__lte': search_date}
                    ).latest('date')
        except ObjectDoesNotExist:
            raise NonExistentGroupError(
                f'''{self.data_model.__name__} with group_id {group_obj.id}
                does not exist at date {search_date}''')

        return data_obj

    def __setManagerObjectDjangoCache(self) -> None:
        """
        Set the current manager object in the Django cache.
        """
        cache_key = f"{self.__class__.__name__}|{self.group_id}"
        cache.set(cache_key, self)

    def updateCache(self) -> None:
        """
        Update the cache for the current instance.
        """
        if self.search_date is None:
            self.__setManagerObjectDjangoCache()

        CacheManager.set_cache_data(
            self.__class__.__name__, 
            self.group_id, self, 
            self.start_date)

    def __getEndDate(self) -> datetime | None:
        return None
        data_obj = self.data_model.objects.filter(
            **{
                self.__group_model_name: self.__group_obj,
                'date__gt': self.start_date
            }
        ).order_by('date').earliest('date') #latest()
        if data_obj:
            return data_obj.date
        return None

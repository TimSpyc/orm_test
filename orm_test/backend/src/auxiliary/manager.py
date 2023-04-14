from exceptions import NonExistentGroupError, NotUpdatableError
import re
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from backend.models import CacheEntry, User
from datetime import datetime
from django.db.models import Max, Model

def transferToSnakeCase(name):
    """
    Convert a string from CamelCase to snake_case.

    Args:
        name (str): The input string in CamelCase.

    Returns:
        str: The output string in snake_case.
    """
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '_', name).lower()

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

    def __new__(cls, group_id=None, search_date=None, use_cache=True):
        """
        Create a new instance of the Manager or return a cached instance if available.

        Args:
            group_id (int, optional): The ID of the group object. Defaults to None for caching only.
            search_date (datetime, optional): The date for which to search the data object. Defaults to None (latest data).
            use_cache (bool, optional): Whether to use the cache when searching for instances. Defaults to True.

        Returns:
            manager: A new or cached instance of the manager.
        """
        manager_name = cls.__name__
        
        if group_id is None:
            return super().__new__(cls)
        if use_cache:
            group_model_name = transferToSnakeCase(cls.group_model.__name__)
            group_model_obj = cls.group_model(group_id)

            if search_date is None:
                cached_instance = cache.get(f"{manager_name}|{group_id}")
                if cached_instance is not None:
                    return cached_instance
            cached_instance = CacheEntry.get_cache_data(manager_name, group_model_obj, group_model_name, cls.data_model, group_id, search_date)
            if cached_instance:
                return cached_instance

        instance = super().__new__(cls)
        instance.__init__(group_id, search_date)
        CacheEntry.set_cache_data(manager_name, group_id, instance, instance.search_date)
        return instance

    def __init__(self, group_id, search_date=None):
        """
        Initialize the manager with the given group_id and date. And save all default attributes.

        Args:
            group_id (int): The ID of the group object.
            search_date (datetime, optional): The date for which to search the data object. Defaults to None (latest data).
        """
        self.__group_model_name = transferToSnakeCase(self.group_model.__name__)
        group_obj = self.__getGroupObject(group_id)
        data_obj = self.__getDataObject(group_obj, search_date)

        self.__group_obj = group_obj
        self.__data_obj = data_obj

        self.id = data_obj.id
        self.group_id = group_obj.id
        self.creator_id = data_obj.creator.id
        self.creator = data_obj.creator
        self.active = data_obj.active
        self.date = data_obj.date

        if search_date is None:
            search_date = datetime.now()
        self.search_date = search_date

        return group_obj, data_obj
    
    @classmethod
    def all(cls, search_date=None):
        """
        Retrieves all objects of the manager's class, optionally filtering by search_date.

        Args:
            search_date (datetime.date, optional): A date to filter the objects by. If specified, only objects with a date less than or equal to the search_date will be included.

        Returns:
            list: A list of manager objects, filtered by the optional search_date if provided.
        """
        return cls.filter(search_date=None)

    @classmethod
    def filter(cls, search_date=None, **kwargs):
        """Creates a list of objects based on the given parameters.

        Keyword arguments:
        search_date (datetime.date, optional) -- An optional argument that specifies the search date for the objects to be created.
        **kwargs: A variable that contains key-value pairs of filter conditions for the database query.

        Returns:
        list -- A list of manager objects that match the filter conditions.

        Example:
        To create a list of all manager objects where the 'name' column is equal to 'foo':
            filter(name='foo')
        """

        group_model_column_list = cls.__getColumnList(cls.group_model)
        data_model_column_list = cls.__getColumnList(cls.data_model)

        group_data_dict, data_data_dict = cls.__getDataForGroupAndDataTableByKwargs(cls, data_model_column_list, group_model_column_list, kwargs)
        return cls.__getFilteredManagerList(group_data_dict, data_data_dict)


    @staticmethod
    def __getDataForGroupAndDataTableByKwargs(cls, data_model_column_list, group_model_column_list, kwargs):
        """
        Separate the input data into group and data dictionaries based on the provided column lists.

        Args:
            data_model_column_list (list): A list of available column names in the data model.
            group_model_column_list (list): A list of available column names in the group model.
            **kwargs: A dictionary of key-value pairs to be searched in the models.

        Returns:
            tuple: A tuple containing:
                - dict: A dictionary containing group model data.
                - dict: A dictionary containing data model data.

        Raises:
            ValueError: If the database column is not unique or has no corresponding column in the models.
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
            
            is_in_group_model, db_column, value = cls.__getValueAndColumnIfExists(db_column, group_model_column_list, cls.group_model, value)
            is_in_data_model, db_column, value = cls.__getValueAndColumnIfExists(db_column, data_model_column_list, cls.data_model, value)
            
            if not is_in_group_model and not is_in_data_model:
                raise ValueError(
                    f'''
                        You can't search data that is not available in DB.
                        {db_column} has no corresponding db column.
                    '''
                )

            elif is_in_group_model:
                group_data_dict[db_column] = value
            elif is_in_data_model:
                data_data_dict[db_column] = value
        
        return group_data_dict, data_data_dict

    @classmethod
    def __getFilteredManagerList(cls, data_search_dict, group_search_dict, search_date=None):
        """
        Get a filtered list of manager instances based on the provided search criteria.

        Args:
            data_search_dict (dict): A dictionary containing data model search criteria.
            group_search_dict (dict): A dictionary containing group model search criteria.
            search_date (datetime, optional): The date to be used for filtering. Defaults to None.

        Returns:
            list: A list of filtered manager instances.
        """
        if search_date is None:
            search_date = datetime.now()

        filter_subsubquery = cls.data_model.objects.filter(date__lt=search_date).values('group_id').annotate(max_date=Max('date')).values('max_date', 'group_id')
        filter_subquery = cls.data_model.objects.filter(**{**{data_search_dict}, 'date__group_id__in': filter_subsubquery}).values('group_id')
        group_id_list = cls.group_model.objects.filter(**{**{group_search_dict}, 'id__in': filter_subquery}).values_list('id', flat=True)

        return [cls(group_id, search_date) for group_id in group_id_list]


    def __errorIfNotUpdatable(self):
        """
        Raise an error if the current instance is not updatable.

        Raises:
            NotUpdatableError: If the current instance is not the latest data in the database.
        """
        latest_db_id = self.data_model.objects.filter(
            **{transferToSnakeCase(self.group_model.__name__): self.__group_obj}
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
    def __searchForColumn(column_name, column_list):
        """
        Search for a given column name in the provided column list and determine if it references a model or many-to-many relationship.

        Args:
            column_name (str): The name of the column to search for.
            column_list (list): A list of available column names.

        Returns:
            tuple: A tuple containing:
                - bool: Whether the column exists in the column list.
                - str: The updated column name if it references a model or many-to-many relationship or the original column name.
                - bool: Whether the column references a model.
                - bool: Whether the column references a many-to-many relationship.
        """
        db_column_exists = False

        column_name, is_reverencing_model = GeneralManager.__checkIfColumnReferencesModel(column_name, column_list)
        column_name, is_many_to_many = GeneralManager.__checkIfColumnReferencesManyToMany(column_name, column_list)

        if column_name in column_list:
            db_column_exists = True

        return db_column_exists, column_name, is_reverencing_model, is_many_to_many

    @staticmethod
    def __checkIfColumnReferencesManyToMany(column_name, available_column_list):
        """
        Check if the given column name references a many-to-many relationship in the provided column list.
        Many-to-many relationship columns must end with '_id_list'.

        Args:
            column_name (str): The name of the column to check.
            available_column_list (list): A list of available column names.

        Returns:
            tuple: A tuple containing:
                - str: The updated column name if it references a many-to-many relationship or the original column name.
                - bool: Whether the column references a many-to-many relationship.
        """
        db_column_is_id = '_id_list' == column_name[-8:]
        is_many_to_many = False
        
        if db_column_is_id:
            db_column_model_name = column_name[:-8]
            if db_column_model_name in available_column_list:
                column_name = db_column_model_name
                is_many_to_many = True
        
        return column_name, is_many_to_many

    @staticmethod
    def __checkIfColumnReferencesModel(column_name, available_column_list):
        """
        Check if the given column name references a model in the provided column list.
        Reference relationship columns must end with '_id'.

        Args:
            column_name (str): The name of the column to check.
            available_column_list (list): A list of available column names.

        Returns:
            tuple: A tuple containing:
                - str: The updated column name if it references a model or the original column name
                - bool: Whether the column references a model.
        """
        db_column_is_id = '_id' == column_name[-3:]
        is_reverencing_model = False
        
        if db_column_is_id:
            db_column_model_name = column_name[:-3]
            if db_column_model_name in available_column_list:
                column_name = db_column_model_name
                is_reverencing_model = True
        
        return column_name, is_reverencing_model
    
    @staticmethod
    def __getValueForReverencedModelById(current_model, db_column, id):
        """
        Retrieve the value of a referenced model by its ID.

        Args:
            current_model (Model): The current Django model.
            db_column (str): The name of the database column.
            id (int): The ID of the referenced model.

        Returns:
            Model: The referenced model object.
        """
        model_for_db_value = (
            current_model._meta.get_field(db_column)
            .remote_field.model
        )
        model_obj = (
            model_for_db_value.objects.filter(id=id).first()
        )
        return model_obj

    @staticmethod
    def __getValueForManyToManyByIdList(current_model, db_column, id_list):
        """
        Retrieve a list of values for a many-to-many relationship by a list of IDs.

        Args:
            current_model (Model): The current Django model.
            db_column (str): The name of the database column.
            id_list (list): A list of IDs for the many-to-many relationship.

        Returns:
            QuerySet: A queryset of related model objects.
        """
        model_for_db_value = (
            current_model._meta.get_field(db_column)
            .remote_field.model
        )
        model_obj_list = (
            model_for_db_value.objects.filter(id__in=id_list)
        )
        return model_obj_list

    @staticmethod
    def __getValueAndColumnIfExists(db_column, model_column_list, model, value):
        """
        Check if a column exists in the model column list and retrieve its value.

        Args:
            db_column (str): The name of the database column.
            model_column_list (list): A list of available column names in the model.
            model (Model): The Django model.
            value: The value associated with the database column.

        Returns:
            tuple: A tuple containing:
                - bool: Whether the column exists in the model column list.
                - str: The updated column name.
                - value: The value associated with the database column.
        """
        is_in_model, db_column, is_reverencing_model, is_many_to_many = GeneralManager.__searchForColumn(
            db_column,
            model_column_list
        )
        if is_reverencing_model:
            value = GeneralManager.__getValueForReverencedModelById(model, db_column, id = value)
        
        if is_many_to_many:
            value = GeneralManager.__getValueForManyToManyByIdList(model, db_column, id_list = value)
        
        return is_in_model, db_column, value

    def __checkInputDictForUpdate(self, db_column, value, available_column_list):
        """
        Check if the input dictionary for updating the model is valid.

        Args:
            db_column (str): The name of the database column.
            value: The value associated with the database column.
            available_column_list (list): A list of available column names in the model.

        Returns:
            tuple: A tuple containing:
                - str: The updated column name.
                - value: The value associated with the database column.

        Raises:
            ValueError: If the database column is not allowed to be updated manually.
        """
        if db_column in [
            'date',
            self.__group_model_name,
            'creator_user_id'
        ]:
            raise ValueError(
                f'''
                    You can't override date and
                    {self.__group_model_name}_id by yourself. Date is
                    always the current date and
                    {self.__group_model_name}_id is unchangeable unless
                    you create a new instance with .create(). The
                    creator_user_id is an extra kwarg because its
                    mandatory and not allowed here.
                '''
            )

        return self.__checkInputDictForCreation(db_column, value, available_column_list)

    def __checkInputDictForCreation(self, db_column, value, available_column_list):
        """
        Check if the input dictionary for creating the model is valid.

        Args:
            db_column (str): The name of the database column.
            value: The value associated with the database column.
            available_column_list (list): A list of available column names in the model.

        Returns:
            tuple: A tuple containing:
                - str: The updated column name.
                - value: The value associated with the database column.

        Raises:
            ValueError: If the database column does not have a corresponding column in the model.
        """
        is_in_model, db_column, value = self.__getValueAndColumnIfExists(db_column, available_column_list, self.data_model, value)

        if not is_in_model:
            raise ValueError(
                f'''
                    You can't push data that is not storable in DB.
                    {db_column} has no corresponding db column.

                '''
            )
        

        return db_column, value
    
    @staticmethod
    def __getColumnList(model):
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
    def update(self, creator_user_id, **kwargs):
        """
        Update the current instance with new data, uploads to db and refresh the cache.

        Args:
            creator_user_id (int): The ID of the user who is making the update.
            **kwargs: Key-value pairs representing the new data to be updated.
        """
        self.__errorIfNotUpdatable()
        data_model_column_list = self.__getColumnList(self.data_model)
        group_model_column_list = [] #Unchangeable by update

        _, data_data_dict = self.__getDataForGroupAndDataTableByKwargs(self, data_model_column_list, group_model_column_list, kwargs)

        group_model_name = transferToSnakeCase(self.group_model.__name__)
        group_model_obj = self.group_model(self.group_id)

        latest_data = self.data_model.objects.filter(**{group_model_name: group_model_obj}).values().latest('date')
        if latest_data == []:
            latest_data = {}

        self.__writeDataData(latest_data, data_data_dict, creator_user_id, self.__group_obj)
        self.__init__(self.group_id)

    @classmethod
    def __writeDataData(cls, latest_data, data_data_dict, creator_user_id, group_obj):
        """
        Write new data to the data model.

        Args:
            latest_data (dict): The latest data fetched from the data model.
            data_data_dict (dict): Dictionary containing the new data to be updated.
            creator_user_id (int): The ID of the user who is making the update.
            group_obj (GroupModel): The group model instance to which the data belongs.
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

        new_data_in_model = cls.data_model(
            **new_data
        )
        new_data_in_model.save()

    def deactivate(self, creator_user_id):
        """
        Deactivate the current instance and set active=False in db.

        Args:
            creator_user_id (int): The ID of the user who is deactivating the instance.
        """
        self.update(creator_user_id, active=False)
    
    @classmethod
    def isDataUploadable(cls, data_dict, model):
        """
        Check if the data provided in the dictionary can be uploaded to the specified model.

        Args:
            data_dict (dict): A dictionary containing the data to be uploaded.
            model (Model): The Django model to which the data should be uploaded.

        Returns:
            tuple: A tuple of three boolean values, each indicating the fulfillment of the following criteria:
                1. Whether all unique fields are present in the data_dict.
                2. Whether all not_null fields are present in the data_dict.
                3. Whether all not_null fields in the data_dict contain data (no None values).
        """
        unique_fields = model._meta.unique_together
        not_null_fields = [field.name for field in model._meta.get_fields() if not field.null and not field.auto_created]

        data_dict_extended_list = list(data_dict.keys())
        data_dict_extended_list.extend(['date', 'creator', 'active', transferToSnakeCase(cls.group_model.__name__)])

        contains_all_unique_fields = set(unique_fields).issubset(set(data_dict_extended_list))
        contains_all_not_null_fields = set(not_null_fields).issubset(set(data_dict_extended_list))
        
        all_not_null_fields_contain_data = not noneValueInNotNullField(not_null_fields, data_dict)


        return (
            contains_all_unique_fields,
            contains_all_not_null_fields,
            all_not_null_fields_contain_data
        )

    @classmethod
    @createCache
    def create(cls, creator_user_id, **kwargs):
        """
        Create a new instance of the current class and initialize cache.

        Args:
            creator_user_id (int): The ID of the user who is creating the new instance.
            **kwargs: Key-value pairs representing the data to be used for creating the new instance.

        Returns:
            cls: A new instance of the current manager class.
        """
        data_model_column_list = cls.__getColumnList(cls.data_model)
        group_model_column_list = cls.__getColumnList(cls.group_model)

        group_data_dict, data_data_dict = cls.__getDataForGroupAndDataTableByKwargs(cls, data_model_column_list, group_model_column_list, kwargs)

        unique_fields = cls.group_model._meta.unique_together

        is_group_data_uploadable = all(cls.isDataUploadable(group_data_dict, cls.group_model))
        is_data_data_uploadable = all(cls.isDataUploadable(data_data_dict, cls.data_model))

        if is_group_data_uploadable and is_data_data_uploadable:

            if len(unique_fields) == 0:
                new_group_obj = cls.group_model(
                    **group_data_dict
                )
            else:
                new_group_obj = self.group_model.objects.get_or_create(
                    **group_data_dict
                )
            new_group_obj.save()

            cls.__writeDataData({}, data_data_dict, creator_user_id, new_group_obj)

            return cls(new_group_obj.id)

        
        else:
            is_group_data_uploadable = cls.isDataUploadable(group_data_dict, cls.group_model)
            is_data_data_uploadable = cls.isDataUploadable(data_data_dict, cls.data_model)
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

    def __getGroupObject(self, group_id):
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
                f"{self.group_model.__name__} with id {group_id} does not exist"
            )
    
    def __getDataObject(self, group_obj, search_date):
        """
        Get the data model instance for the given group object and date.

        Args:
            group_obj (GroupModel): The group model instance for which the data is to be fetched.
            search_date (datetime): The date for which the data is to be fetched.

        Returns:
            DataModel: The data model instance for the given group object and date.
        """
        try:
            if search_date is None:
                data_obj = self.data_model.objects.filter(
                    **{self.__group_model_name: group_obj}
                ).latest('date')
            else:
                data_obj = self.data_model.objects.filter(
                    **{self.__group_model_name: group_obj, 'date__lte': search_date}
                ).latest('date')
        except ObjectDoesNotExist:
            raise NonExistentGroupError(
                f"{self.data_model.__name__} with group_id {group_obj.id} does not exist at date {search_date}")

        return data_obj
    
    def __setManagerObjectDjangoCache(self):
        """
        Set the current manager object in the Django cache.
        """
        cache_key = f"{self.__class__.__name__}|{self.group_id}"
        cache.set(cache_key, self)

    def updateCache(self):
        """
        Update the cache for the current instance.
        """
        if self.search_date is None:
            self.__setManagerObjectDjangoCache()
        CacheEntry.set_cache_data(self.__class__.__name__, self.group_id, self, self.search_date)

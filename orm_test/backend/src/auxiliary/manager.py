from backend import models
from backend.src.auxiliary.exceptions import NonExistentGroupError, NotUpdatableError, NotValidIdError
import re
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from backend.models import CacheManager, User
from datetime import datetime
from django.db.models import Model, Field
from django.db.models.query import QuerySet
from django.db import models
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.fields import NOT_PROVIDED


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
    data_extension_model_list: list[Model]

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

        if hasattr(cls, 'group_model'):
            group_table_id_name = f'''
                {transferToSnakeCase(cls.group_model.__name__)}_id
            '''
            if group_table_id_name in kwargs:
                group_id = kwargs[group_table_id_name]
        
        if group_id is None:
            return super().__new__(cls)

        if use_cache:
            cached_instance = cls.__handleCache(group_id, search_date)
            if cached_instance:
                return cached_instance

        instance = super().__new__(cls)
        instance.__init__(group_id, search_date)
        cls.updateCache(instance)

        return instance

    def __init__(
        self,
        group_id: int,
        search_date: datetime|None = None,
        use_cache: bool = True
    ):
        """
        Initialize the manager with the given group_id and date.
        And save all default attributes.

        Args:
            group_id (int): The ID of the group object.
            search_date (datetime, optional): The date for which to search
                the data object. Defaults to None (latest data).
        """
        self.use_cache = use_cache
        self.search_date = search_date
        self.group_id = group_id

        self.__group_model_name = self.__getGroupModelName()
        group_obj = self.__getGroupObject()
        data_obj = self.__getDataObject(group_obj, search_date)

        self.__group_obj = group_obj
        self.__data_obj = data_obj

        self.id = data_obj.id
        ignore_list = [
            self.__group_model_name,
            'id',
            'date'
        ]
        self.__setAllAttributesFromModel(group_obj, ignore_list)
        self.__setAllAttributesFromModel(data_obj, ignore_list)

        self.start_date = data_obj.date
        self.end_date = self.__getEndDate()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.group_id}, {self.search_date})'

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if isinstance(value, Model):
                value_dict = value.__dict__
                for key, value in value_dict.items():
                    attr_with_key = f'{attr}__{key}'
                    yield attr_with_key, value
            yield attr, value

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__) and
            self.group_id == other.group_id and
            self.start_date == other.start_date
        )

    def __setAllAttributesFromModel(
        self,
        model_obj: Model,
        ignore_list: list = []
    ) -> None:

        for column in model_obj._meta.get_fields():
            ref_table_type, ref_type = self.__getRefAndTableType(column)
            column_name = column.name

            if self.__isIgnored(column_name, ignore_list):
                continue

            if ref_table_type is None:
                self.__createDirectAttribute(column_name, column, model_obj)
            else:
                self.__createReferenceAttribute(
                    column_name, column, model_obj, ref_table_type, ref_type
                )

    def __createDirectAttribute(
        self,
        column_name: str,
        column: Field,
        model_obj: Model
    ) -> None:
        setattr(self, column_name, getattr(model_obj, column.name))

    @staticmethod
    def __get_fields_and_values(instance):
        fields = {}
        for field in instance._meta.fields:
            value = getattr(instance, field.name)
            fields[field.name] = value
        for field in instance._meta.many_to_many:
            fields[field.name] = list(
                getattr(instance, field.name).all()
            )
        return fields

    def __createReferenceAttribute(
        self,
        column_name: str,
        column: Field,
        model_obj: Model,
        ref_table_type: str,
        ref_type: str
    ) -> None:

        def getManagerListFromGroupModel():
            return [
                group_data.manager(self.search_date, self.use_cache)
                for group_data in getattr(model_obj, column.name).all()
            ]
        
        def getManagerListFromDataModel():
            manager_list = []
            for data_data in getattr(model_obj, column.name).all(): 
                group_data = data_data.group
                manager = group_data.manager(self.search_date, self.use_cache)
                if manager.id == data_data.id:
                    manager_list.append(manager)
            return manager_list

        def getExtensionDataDict():
            return [
                self.get_fields_and_values(instance)
                for instance in getattr(model_obj, column.name).all()
            ]

        def getManagerFromGroupModel():
            group_data = getattr(model_obj, column.name)
            return group_data.manager(self.search_date, self.use_cache)

        def getManagerFromDataModel():
            data_data = getattr(model_obj, column.name)
            group_data = data_data.group
            manager = group_data.manager(self.search_date, self.use_cache)
            if manager.id == data_data.id:
                return manager

        if ref_type == 'ManyToManyField' or ref_type == 'ManyToOneRel':
            if ref_table_type == 'GroupTable':
                attribute_name = column_name.replace('group', 'manager_list')
                self.__createProperty(
                    attribute_name,
                    getManagerListFromGroupModel
                )
            elif ref_table_type == 'DataExtensionTable':
                attribute_name = f'{column_name}_dict_list'
                setattr(self, attribute_name, getExtensionDataDict())

            elif ref_table_type == 'DataTable':
                if self.data_model == column.related_model:
                    return
                attribute_name = f"{column_name}_manager"
                self.__createProperty(
                    attribute_name,
                    getManagerListFromDataModel
                )
            else:
                raise ValueError('this is not implemented yet')
        elif ref_type == 'ForeignKey':
            if ref_table_type == 'GroupTable':
                attribute_name = column_name.replace('group', 'manager')
                self.__createProperty(
                    attribute_name,
                    getManagerFromGroupModel
                )
            elif ref_table_type == 'ReferenceTable':
                foreign_key_object = getattr(model_obj, column.name)
                setattr(self, column_name, foreign_key_object)
            elif ref_table_type == 'DataTable':
                if self.data_model == column.related_model:
                    return
                attribute_name = f"{column_name}_manager"
                self.__createProperty(
                    attribute_name,
                    getManagerFromDataModel
                )
            elif ref_table_type == 'DataExtensionTable':
                raise ValueError(
                    'Your database model is not correctly implemented!!'
                )
            else:
                raise ValueError('this is not implemented yet')

    def __createProperty(self, attribute_name: str, func):
        setattr(self.__class__, attribute_name, property(func))

    @staticmethod
    def __isIgnored(key: str, ignore_list: list) -> bool:
        if key in ignore_list:
            return True
        return False

    @staticmethod
    def __getRefAndTableType(column: Field) -> tuple[str, str]:
        """
        Get the reference table type and field type of a column.

        Args:
            column (Field): The field object to analyze.

        Returns:
            tuple[str, str]: A tuple containing the ref table type and ref type.
         """
        
        if column.related_model:
            ref_table_type = column.related_model.table_type
            ref_type = column.get_internal_type()
            if isinstance(column, ManyToOneRel):
                ref_type = "ManyToOneRel"
        else:
            ref_table_type = None
            ref_type = None
        return ref_table_type, ref_type
    

    @classmethod
    def __getGroupModelName(cls) -> str:
        """
        Get group model name. Raises value error if group model name 
        is not in data model columns!
        Returns:
            group_model_name
        """
        column_list = cls.__getColumnNameList(cls.data_model)
        group_model_name = transferToSnakeCase(cls.group_model.__name__)
        db_column_exists, *_ = cls.\
        __searchForColumn(group_model_name, column_list)
        
        if not db_column_exists:
            raise ValueError (
                f'''the column {group_model_name} does not exist 
                in your data model ({cls.data_model})!''')
        
        return group_model_name

    @classmethod
    def all(cls, search_date=None, use_cache=True) -> list:
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
        return cls.filter(search_date=search_date, use_cache=use_cache)

    @classmethod
    def filter(cls, search_date=None, use_cache=True, **kwargs: any) -> list:
        """Creates a list of objects based on the given parameters.
        It's NOT possible to search for DataExtensionTable Data.

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

        group_model_column_list = cls.__getColumnNameList(cls.group_model)
        data_model_column_list = cls.__getColumnNameList(cls.data_model)

        group_data_dict, data_data_dict, data_extension_data_dict = cls.\
            __getDataForGroupAndDataTableByKwargs(
            data_model_column_list,
            group_model_column_list, 
            **kwargs
            )
        if data_extension_data_dict != {}:
            raise ValueError(f'''
                It's not possible to search for data in data extension tables
                yet. You have searched for {data_extension_data_dict}.
            ''')
        found_group_id_date_combination_dict_list = cls.\
            __getFilteredManagerList(
            data_data_dict,
            group_data_dict, 
            search_date
            )
        return cls.__createManagerObjectsFromDictList(
            found_group_id_date_combination_dict_list,
            use_cache=use_cache
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
        data_extension_data_dict = {}
        for _db_column, _value in kwargs.items():
            key = _db_column
            value = _value
            if _db_column in not_unique_column_names:
                raise ValueError(
                    f'''
                        It's not possible to search for {_db_column} because
                        the value exists in group and data model.
                    '''
                )
            is_in_group_model, key, value = cls.__getValueAndColumnIfExists(
                key, 
                group_model_column_list, 
                cls.group_model,
                value
                )
            is_in_data_model, key, value = cls.__getValueAndColumnIfExists(
                key, 
                data_model_column_list, 
                cls.data_model, 
                value
                )
            is_in_data_ext_model, key, value = cls.__getDataExtensionData(
                key,
                value
            )

            if not any(
                [is_in_group_model, is_in_data_model, is_in_data_ext_model]
            ):
                raise ValueError(
                    f'''
                     You can't search/create data that is not available in DB.
                     {key} has no corresponding db column.
                    '''
                )

            elif is_in_group_model:
                group_data_dict[key] = value
            elif is_in_data_model:
                data_data_dict[key] = value
            elif is_in_data_ext_model:
                data_extension_data_dict[key] = value

        return group_data_dict, data_data_dict, data_extension_data_dict


    @classmethod
    def __getDataExtensionData(
        cls,
        key: str,
        value: any
    ) -> tuple[bool, str, any]:
        is_in_data_ext_model = False
        if not type(value) == list:
            return is_in_data_ext_model, key, value

        possible_models = {
            model.__name__: model
            for model in cls.data_extension_model_list
        }
        model_name, is_reverencing_data_ext = \
            cls.__checkIfColumnReferencesDataExtensionModel(
                key,
                list(possible_models.keys())
            )
        if not is_reverencing_data_ext:
            return is_in_data_ext_model, key, value
        
        referenced_model = possible_models[model_name]
        referenced_model_column_list = cls.__getColumnNameList(
            referenced_model
        )
        to_upload_dict = {
            'referenced_model': referenced_model,
            'data': []
        }
        is_in_data_ext_model = True
        for data_dict in value:
            to_insert_dict = {}
            for key in data_dict:
                is_in_referenced_model, key, value = \
                    cls.__getValueAndColumnIfExists(
                        key, 
                        referenced_model_column_list, 
                        referenced_model, 
                        value
                        )
                
                if not is_in_referenced_model:
                    raise ValueError(
                        f'''
                        You can't create data that is not available in DB.
                        {key} has no corresponding db column in model {referenced_model}.
                        '''
                    )
                to_insert_dict[key] = value
            
            to_upload_dict['data'].append(to_insert_dict)

        return is_in_data_ext_model, model_name, to_upload_dict


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
        creation_dict_list: list,
        use_cache
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
        return [cls(**data, use_cache=use_cache) for data in creation_dict_list] 

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

        return (
            db_column_exists,
            column_name,
            is_reverencing_model,
            is_many_to_many,
        )

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
        is_referencing_model = False
        
        if db_column_contains_string_to_compare:
            db_column_model_name = column_name[:negative_length_to_cut]
            if db_column_model_name in available_column_list:
                column_name = db_column_model_name
                is_referencing_model = True
        
        return column_name, is_referencing_model

    @staticmethod
    def __checkIfColumnReferencesDataExtensionModel(
        column_name: str, 
        possible_models: list
    ) -> tuple[str,bool]:
        """
        Check if the given column name references a DataTable Model
        in the provided possible models list. DataExtensions relationship columns 
        must end with '_dict_list'.

        Args:
            column_name (str): The name of the column to check.
            possible_models (list): A list of available models.

        Returns:
            Tuple: 
                The modified column name and a boolean if is_referencing_model.
        """
        return  GeneralManager.__checkIfColumnReferenceBaseExists(
            column_name, 
            possible_models,
            "_dict_list"
        )

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
            available_column_list,
            "_id_list"
        )

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
            available_column_list,
            "_id"
        )

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
            raise NotValidIdError(f"""
                {model_for_db_value} with id {id} does not exist.
            """)
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
            raise NotValidIdError(f'''
                One or more IDs in the list do not exist 
                in the database: {not_existing_ids}
            ''')                                                           
        
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
        (is_in_model,
         db_column,
         is_reverencing_model,
         is_many_to_many) = GeneralManager.__searchForColumn(
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
    def __getColumnNameList(model: models.Model) -> list:
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
        data_model_column_list = self.__getColumnNameList(self.data_model)
        group_model_column_list = [] #Unchangeable by update
        self.__checkInputDictForInvalidKeys(
            manager_object = self,
            column_list = kwargs.keys(),
            invalid_key_list = self.__getToCheckListForUpdate()
        )

        _, data_data_dict, data_extension_data_dict = self.\
            __getDataForGroupAndDataTableByKwargs(
                data_model_column_list, 
                group_model_column_list, 
                **kwargs
                )
        is_data_extension_data_uploadable = self.__isDataExtensionUploadable(
            data_extension_data_dict
        )
        if is_data_extension_data_uploadable:
            latest_data_data = self.__getLatestDataData()
            latest_extension_data = self.__getLatestDataExtensionData()

            self.__writeData(
                latest_data_data,
                data_data_dict,
                creator_user_id, 
                self.__group_obj,
                datetime.now(),
                latest_extension_data,
                data_extension_data_dict,
            )

            self.__init__(self.group_id)
    
    @classmethod
    def __writeData(
        cls, 
        latest_data_data: dict, 
        data_data_dict: dict,
        creator_user_id: int, 
        group_obj: models.Model,
        latest_extension_data: dict,
        data_extension_data_dict: dict,
    ) -> None:

        new_data_model_obj = cls.__writeDataData(
            latest_data_data,
            data_data_dict,
            creator_user_id, 
            group_obj,
            datetime.now()
        )

        cls.__writeDataExtensionData(
            latest_extension_data,
            data_extension_data_dict,
            new_data_model_obj
        )

    def __getLatestDataData(self):
        group_model_name = transferToSnakeCase(self.group_model.__name__)
        group_model_obj = self.__group_obj
        latest_data = self.data_model.objects.filter(
            **{group_model_name: group_model_obj}
            ).values().latest('date')
        if latest_data == []:
            latest_data = {}
        return latest_data
    
    def __getLatestDataExtensionData(self):
        latest_extension_data = {}
        for data_extension_model in self.data_extension_model_list:
            data_extension_model_name = data_extension_model.__name__
            data_model_name = transferToSnakeCase(self.data_model.__name__)
            data_model_obj = self.__data_obj
            latest_data = data_extension_model.objects.filter(
                **{data_model_name: data_model_obj}
                ).values()

            latest_extension_data[data_extension_model_name] = []
            for entry in latest_data:
                data_dict = self.__get_fields_and_values(entry)
                latest_extension_data[data_extension_model_name].append(data_dict)

        return latest_extension_data

    @classmethod
    def __writeDataData(
        cls, 
        latest_data: dict, 
        data_data_dict: dict,
        creator_user_id: int, 
        group_obj: models.Model
    ) -> models.Model:
        """
        Write new data to the data model and data extension models.

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

        new_data_model_obj = cls.__saveDataToDB(cls.data_model, new_data)

        return new_data_model_obj

    @staticmethod
    def __getToPushListForDataExtensionData(
        data_extension_model: Model,
        data_extension_data_dict: dict,
        latest_extension_data: dict,
        new_data_model_obj: Model
    ) -> dict:

        data_extension_model_name = data_extension_model.__name__
        data_table_name = transferToSnakeCase(
            new_data_model_obj.__class__.__name__
        )
        
        if data_extension_model_name in data_extension_data_dict:
            dict_to_use = data_extension_data_dict
        else:
            dict_to_use = latest_extension_data
        
        return [
            {
                **data_dict,
                **{
                    data_table_name: new_data_model_obj
                }
            }
            for data_dict in dict_to_use[data_extension_model_name]
        ]

    @classmethod
    def __writeDataExtensionData(
        cls,
        latest_extension_data: dict,
        data_extension_data_dict: dict,
        new_data_model_obj: models.Model
    ) -> None:
        """
        Write new data to the data model and data extension models.

        Args:
            latest_extension_data (dict):
                The latest data fetched from the data extension models.
            data_extension_data_dict (dict): 
                Dictionary containing the new data to be updated.
            creator_user_id (int): The ID of the user who is making the update.
            group_obj (GroupModel): 
                The group model instance to which the data belongs.
        """
        data_table_name = transferToSnakeCase(cls.data_model.__name__)
        
        for data_extension_model in cls.data_extension_model_list:
            to_push_data_list = cls.__getToPushListForDataExtensionData(
                data_extension_model,
                data_extension_data_dict,
                latest_extension_data,
                new_data_model_obj
            )
            for to_push_data in to_push_data_list:
                try:
                    del to_push_data['id']
                except KeyError:
                    pass

                cls.__saveDataToDB(
                    data_extension_model,
                    to_push_data
                )

    @staticmethod
    def __saveDataToDB(model_to_insert, new_data):
        many_to_many_dict = {}
        not_many_to_many_dict = {}
        
        for key, value in new_data.items():
            if type(value) == QuerySet:
                many_to_many_dict[key] = value
            else:
                not_many_to_many_dict[key] = value

        new_data_model_obj = model_to_insert(
            **not_many_to_many_dict
        )
        new_data_model_obj.save()

        for key, value_list in many_to_many_dict.items():
            for value in value_list:
                getattr(new_data_model_obj, key).add(value)
        
        new_data_model_obj.save()

        return new_data_model_obj

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

    @staticmethod
    def __getNotNullFields(model):
        return [
            field.name for field in model._meta.get_fields()
            if not field.null and not field.auto_created and
            field.default == NOT_PROVIDED
        ]

    @staticmethod
    def __getUniqueFields(model):
        unique_fields = []
        for unique_field_tuple in model._meta.unique_together:
            unique_fields = [*unique_field_tuple, *unique_fields]
        return unique_fields

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
        not_null_fields = cls.__getNotNullFields(model)
        unique_fields = cls.__getUniqueFields(model)
        
        data_dict_extended_list = list(data_dict.keys())
        data_dict_extended_list.extend([
            'date', 
            'creator', 
            'active', 
            transferToSnakeCase(cls.group_model.__name__),
            transferToSnakeCase(cls.data_model.__name__),
        ])
        
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
    def __errorForInsufficientUploadData(cls, model_type: str, is_data_uploadable: list):
        if model_type == 'data_model':
            name = 'data table data'
            model = cls.data_model
        elif model_type == 'group_model':
            name = 'group table data'
            model = cls.group_model
        raise ValueError(
            f'''
            The given **kwargs are not sufficient.
            Because {name}:
                contains_all_unique_fields: {is_data_uploadable[0]}
                contains_all_not_null_fields: {is_data_uploadable[1]}
                all_not_null_fields_contain_data: {is_data_uploadable[2]}
            For data model: {model}
                not_null_fields = {cls.__getNotNullFields(model)}
                unique_fields = {cls.__getUniqueFields(model)}
            '''
        )

    @classmethod
    def __isDataDataUploadable(cls, data_data_dict):
        is_data_data_uploadable = cls.__isDataUploadable(
                                    data_data_dict, 
                                    cls.data_model)
        if all(is_data_data_uploadable):
            return True
        cls.__errorForInsufficientUploadData(
            'data_model', is_data_data_uploadable
        )

    @classmethod
    def __isGroupDataUploadable(cls, group_data_dict):
        is_group_data_uploadable = cls.__isDataUploadable(
                                    group_data_dict, 
                                    cls.group_model)
        if all(is_group_data_uploadable):
            return True
        cls.__errorForInsufficientUploadData(
            'group_model', is_group_data_uploadable
        )
    
    @classmethod
    def __isDataExtensionUploadable(
        cls,
        data_extension_data_dict
    ):
        is_data_extension_data_uploadable = True
        for data_extension_model in cls.data_extension_model_list:
            is_valid = cls.__checkIfDataExtensionIsUploadable(
                data_extension_model,
                data_extension_data_dict
            )
            is_data_extension_data_uploadable = all(
                is_data_extension_data_uploadable, is_valid
            )
        return is_data_extension_data_uploadable

    @classmethod
    def __checkIfDataExtensionIsUploadable(
        cls,
        data_extension_model: Model,
        data_extension_data_dict: dict
    ):
        data_extension_model_name = data_extension_model.__name__
        if data_extension_model_name not in data_extension_data_dict.keys():
            return True
        data_to_check = data_extension_data_dict[data_extension_model_name]
        is_data_extension_data_uploadable = cls.__isDataUploadable(
            data_to_check, 
            data_extension_model
        )
        if all(is_data_extension_data_uploadable):
            return True
        cls.__errorForInsufficientUploadData(
            'data_extension_model_name', is_data_extension_data_uploadable
        )

    @classmethod
    def __getOrCreateGroupModel(cls, group_data_dict):
        unique_fields = cls.group_model._meta.unique_together

        if len(unique_fields) == 0:
            group_obj = cls.group_model.object.create(
                **group_data_dict
            )
        else:
            group_obj, _ = cls.group_model.objects.get_or_create(
                **group_data_dict
            )

        return group_obj

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
        data_model_column_list = cls.__getColumnNameList(cls.data_model)
        group_model_column_list = cls.__getColumnNameList(cls.group_model)
        cls.__checkInputDictForInvalidKeys(
            manager_object = cls,
            column_list = kwargs.keys(),
            invalid_key_list = cls.__getToCheckListForCreation()
        )
        group_data_dict, data_data_dict, data_extension_data_dict=cls.\
        __getDataForGroupAndDataTableByKwargs(
            data_model_column_list, 
            group_model_column_list, 
            **kwargs)

        is_group_data_uploadable = cls.__isDataDataUploadable(group_data_dict)
        is_data_data_uploadable = cls.__isGroupDataUploadable(data_data_dict)
        is_data_extension_data_uploadable = cls.__isDataExtensionUploadable(
            data_extension_data_dict
        )

        if all(
            is_group_data_uploadable,
            is_data_data_uploadable,
            is_data_extension_data_uploadable
        ):
            group_obj = cls.__getOrCreateGroupModel(group_data_dict)

            cls.__writeData(
                {},
                data_data_dict,
                creator_user_id, 
                group_obj,
                datetime.now(),
                {},
                data_extension_data_dict,
            )

            return cls(group_obj.id)

    def __getGroupObject(self) -> models.Model:
        """
        Get the group model instance with the provided group ID.

        Args:
            group_id (int): The ID of the group model instance to be fetched.

        Returns:
            GroupModel: The group model instance with the provided ID.
        """
        try:
            return self.group_model.objects.get(id=self.group_id)
        except ObjectDoesNotExist:
            raise NonExistentGroupError(
                f'''{self.group_model.__name__} with 
                    id {self.group_id} does not exist'''
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

    @classmethod
    def __handleCache(cls, group_id, search_date):
            
        manager_name = cls.__name__
        group_model_name = transferToSnakeCase(cls.group_model.__name__)
        group_model_obj = cls.group_model(group_id)

        if search_date is None:
            cached_instance = cache.get(f"{manager_name}|{group_id}")
            if cached_instance:
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
        return None

    def __getEndDate(self) -> datetime | None:
        """
        Get end date for data validity. As the data in the data table can
        change over time it's unavoidable that in some point in time the data
        is outdated. Sets this date as end_date.

        Returns:
            end_date: (datetime) if there is a end_date. (None) if there is no
                newer entry for this group in the data table.
        """
        try:
            data_obj = self.data_model.objects.filter(
                **{
                    self.__group_model_name: self.__group_obj,
                    'date__gt': self.start_date
                }
            ).earliest('date') #latest()
            return data_obj.date
        except ObjectDoesNotExist:
            return None

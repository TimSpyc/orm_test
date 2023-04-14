from exceptions import NonExistentGroupError, NotUpdatableError
import re
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from backend.models import CacheEntry
from datetime import datetime
from django.db.models import Max, Model

def transferToSnakeCase(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def noneValueInNotNullField(not_null_fields, data_dict):
    data_is_none_list = []
    for key, data in data_dict:
        if data is None:
            data_is_none_list.append(key)
    
    return bool(set(not_null_fields).insersection(set(data_dict.keys())))

def updateCache(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.updateCache()

        return result
    return wrapper

def createCache(func):
    def wrapper(cls, *args, **kwargs):
        result = func(cls, *args, **kwargs)
        result.updateCache()

        return result
    return wrapper


class GeneralManager:

    group_model = Model
    data_model = Model

    def __new__(cls, group_id=None, date=None, use_cache=True):
        manager_name = cls.__name__
        
        if group_id is None:
            return super().__new__(cls)
        if use_cache:
            group_model_name = transferToSnakeCase(cls.group_model.__name__)
            group_model_obj = cls.group_model(group_id)

            if date is None:
                cached_group_obj = cache.get(f"{manager_name}|{group_id}")
            cached_instance = CacheEntry.get_cache_data(manager_name, group_model_obj, group_model_name, cls.data_model, group_id, date)
            if cached_instance:
                return cached_instance

        instance = super().__new__(cls)
        instance.__init__(group_id, date)
        CacheEntry.set_cache_data(manager_name, group_id, instance, instance.date)
        return instance

    def __init__(self, group_id, date=None):
        self.__group_model_name = transferToSnakeCase(self.group_model.__name__)
        group_obj = self.__getGroupObject(group_id)
        data_obj = self.__getDataObject(group_obj, date)

        self.__group_obj = group_obj
        self.__data_obj = data_obj

        self.id = data_obj.id
        self.group_id = group_obj.id
        self.creator_id = data_obj.creator.id
        self.creator = data_obj.creator
        self.active = data_obj.active
        self.date = data_obj.date

        if date is None:
            date = datetime.now()
        self.search_date = date

        return group_obj, data_obj
    
    @classmethod
    def getAll(cls, date=None, **kwargs):
        """Creates a list of objects based on the given parameters.

        Keyword arguments:
        date (datetime.date, optional) -- An optional argument that specifies the date for the objects to be created.
        **kwargs: A variable that contains key-value pairs of filter conditions for the database query.

        Returns:
        list -- A list of objects that match the filter conditions.

        Example:
        To create a list of all objects where the 'name' column is equal to 'foo':
            getAll(name='foo')
        """

        group_model_column_list = cls.__getColumnList(cls.group_model)
        data_model_column_list = cls.__getColumnList(cls.data_model)

        group_data_dict, data_data_dict = cls.__getDataForGroupAndDataTableByKwargs(data_model_column_list, group_model_column_list, kwargs)
        return cls.__getFilteredManagerList(group_data_dict, data_data_dict)


    @classmethod
    def __getDataForGroupAndDataTableByKwargs(cls, data_model_column_list, group_model_column_list, **kwargs):

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
    def __getFilteredManagerList(cls, data_search_dict, group_search_dict, date=None):
        search_date = date
        if search_date is None:
            search_date = datetime.now()

        filter_subsubquery = cls.data_model.objects.filter(date__lt=date).values('group_id').annotate(max_date=Max('date')).values('max_date', 'group_id')
        filter_subquery = cls.data_model.objects.filter(**{**{data_search_dict}, 'date__group_id__in': filter_subsubquery}).values('group_id')
        group_id_list = cls.group_model.objects.filter(**{**{group_search_dict}, 'id__in': filter_subquery}).values_list('id', flat=True)

        return [cls(group_id, date) for group_id in group_id_list]


    def errorIfNotUpdatable(self):
        latest_db_id = self.data_model.objects.filter(
            **{transferToSnakeCase(self.group_model.__name__): group_obj}
        ).values('id')

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
        db_column_exists = False

        column_name, is_reverencing_model = GeneralManager.__checkIfColumnReferencesModel(column_name, column_list)
        column_name, is_many_to_many = GeneralManager.__checkIfColumnReferencesManyToMany(column_name, column_list)

        if column_name in column_list:
            db_column_exists = True

        return db_column_exists, column_name, is_reverencing_model, is_many_to_many

    @staticmethod
    def __checkIfColumnReferencesManyToMany(column_name, available_column_list):
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
        model_for_db_value = (
            current_model._meta.get_field(db_column)
            .remote_field.model
        )
        model_obj_list = (
            model_for_db_value.objects.filter(id__in=list_of_ids)
        )
        return model_obj

    @staticmethod
    def __getValueAndColumnIfExists(db_column, model_column_list, model, value):
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
        column_list = [field.name for field in model._meta.get_fields()]
        return column_list

    @updateCache
    def update(self, creator_user_id, **kwargs):
        self.errorIfNotUpdatable()
        data_model_column_list = self.__getColumnList(self.data_model)
        group_model_column_list = [] #Unchangeable by update

        _, data_data_dict = self.__getDataForGroupAndDataTableByKwargs(data_model_column_list, group_model_column_list, kwargs)

        latest_data = self.data_model.objects.values().latest('date')

        self.__writeDataData(latest_data, data_data_dict, creator_user_id, self.__group_obj)
        self.__init__()

    @classmethod
    def __writeDataData(cls, latest_data, data_data_dict, creator_user_id, group_obj):
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

        new_data_in_model = self.data_model(
            **new_data
        )
        new_data_in_model.save()

    def deactivate(self, creator_user_id):
        self.update(active=False)
    
    @staticmethod
    def isDataUploadable(data_dict, model, compact=True):

        unique_fields = model._meta.unique_together
        not_null_fields = [field for field in model._meta.get_fields() if not field.null and not field.auto_created]
        
        contains_all_unique_fields = set(unique_fields).issubset(set(data_dict.keys()))
        contains_all_not_null_fields = set(not_null_fields).issubset(set(data_dict.keys()))
        
        all_not_null_fields_contain_data = noneValueInNotNullField(not_null_fields, data_dict)

        if compact:
            return (
                contains_all_unique_fields and
                contains_all_not_null_fields and
                all_not_null_fields_contain_data
            )
        else:
            return (
                contains_all_unique_fields,
                contains_all_not_null_fields,
                all_not_null_fields_contain_data
            )

    @classmethod
    @createCache
    def create(cls, creator_user_id, **kwargs):
        data_model_column_list = cls.__getColumnList(cls.data_model)
        group_model_column_list = cls.__getColumnList(cls.group_model)

        group_data_dict, data_data_dict = cls.__getDataForGroupAndDataTableByKwargs(data_model_column_list, group_model_column_list, kwargs)

        unique_fields = cls.group_model._meta.unique_together

        is_group_data_uploadable = cls.isDataUploadable(group_data_dict, cls.group_model)
        is_data_data_uploadable = cls.isDataUploadable(data_data_dict, cls.data_model)

        if is_group_data_uploadable and is_data_data_uploadable:

            if len(unique_fields) == 0:
                new_group_obj = self.group_model(
                    **group_data_dict
                )
            else:
                new_group_obj = self.group_model.objects.get_or_create(
                    **group_data_dict
                )
            new_group_obj.save()

            cls.__writeDataData([], data_data_dict, creator_user_id, new_group_obj)

            return cls(new_group_obj.id)

        
        else:
            is_group_data_uploadable = cls.isDataUploadable(group_data_dict, cls.group_model, compact=False)
            is_data_data_uploadable = cls.isDataUploadable(data_data_dict, cls.data_model, compact=False)
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
        try:
            return self.group_model.objects.get(id=group_id)
        except ObjectDoesNotExist:
            raise NotUpdatableError(
                f"{self.group_model.__name__} with id {group_id} does not exist"
            )
    
    def __getDataObject(self, group_obj, date):
        try:
            if date is None:
                data_obj = self.data_model.objects.filter(
                    **{self.__group_model_name: group_obj}
                ).latest('date')
            else:
                data_obj = self.data_model.objects.filter(
                    **{self.__group_model_name: group_obj, 'date__lte': date}
                ).latest('date')
        except ObjectDoesNotExist:
            raise NonExistentGroupError(
                f"{self.data_model.__name__} with group_id {group_id} does not exist at date {date}")

        return data_obj
    
    def __setManagerObjectDjangoCache(self):
        cache_key = f"{self.__class__.__name__}|{self.group_id}"
        cache.set(cache_key, self)

    def updateCache(self):
        if self.search_date is None:
            self.__setManagerObjectDjangoCache()
        CacheEntry.objects.set_cache_data(self.__class__.__name__, self.group_id, self, self.date)

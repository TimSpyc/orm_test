from exceptions import NonExistentGroupError, NotUpdatableError
import re
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from backend.models import CacheEntry
from datetime import datetime

def transferToSnakeCase(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

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
    def __new__(cls, group_id, date=None, use_cache=True):
        if use_cache:
            manager_name = cls.__name__
            if date is None:
                cached_group_obj = cache.get(f"{manager_name}|{group_id}")
            cached_instance = CacheEntry.objects.get_cache_data(manager_name, cls.data_model, group_id, date)
            if cached_instance:
                return cached_instance

        instance = super().__new__(cls)
        instance.__init__(group_id, date)
        CacheEntry.objects.set_cache_data(manager_name, group_id, instance, instance.date)
        return instance

    def __init__(self, group_id, date=None):
        self.__group_model_name = transferToSnakeCase(self.group_model.__name__)
        group_obj = self.__getGroupObject(group_id)
        data_obj = self.__getDataObject(group_obj, date)

        self.__group_obj = group_obj
        self.__data_obj = data_obj

        self.id = data_obj.id
        self.group_id = group_obj.id
        self.creator_user_id = data_obj.creator.id
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
        return [
            cls(group_id, date) for group_id in
            cls.group_model.objects.get(**kwargs).values_list('id', flat=True)
        ]

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
    def __checkIfColumnReferencesModel(db_column, available_column_list):
        db_column_is_id = '_id' == db_column[-3:]
        is_reverencing_model = False
        
        if db_column_is_id:
            db_column_model_name = db_column[:-3]
            if db_column_model_name in available_column_list:
                db_column = db_column_model_name
                is_reverencing_model = True
        
        return db_column, is_reverencing_model
    
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

        db_column, is_reverencing_model = self.__checkIfColumnReferencesModel(db_column, available_column_list)

        if is_reverencing_model:
            value = self.__getValueForReverencedModelById(self.group_model, db_column, id = value)
        
        elif db_column not in available_column_list:
            raise ValueError(
                f'''
                    You can't push data that is not storable in DB.
                    {db_column} has no corresponding db column.

                '''
            )

        return db_column, value


    @updateCache
    def update(self, creator_user_id, **kwargs):
        self.errorIfNotUpdatable()

        latest_data = self.data_model.objects.filter(
            **{self.__group_model_name:self.__group_obj}
        ).latest('id').values()
        column_list = list(latest_data.keys())


        changed_data = {}
        for _db_column, _value in kwargs.items():
            db_column, value = self.__checkInputDictForUpdate(_db_column, _value, column_list)
            changed_data[db_column] = value

        new_data = {
            **latest_data,
            **changed_data,
            **{
                'date': datetime.now(),
                'creator':User.objects.get(id=creator_user_id),
                self.__group_model_name: self.group_id
            }
        }

        new_data_in_model = self.data_model(
            **new_data
        )
        new_data_in_model.save()
        self.__init__()

    def deactivate(self, creator_user_id):
        self.update(active=False)
    
    # @classmethod
    # @createCache
    # def create(cls, creator_user_id, **kwarg):
    #     unique_fields = self.group_model._meta.unique_together

    #     if len(unique_fields) == 0:
    #         new_group = self.group_model()
    #         new_group.save()
    #     else:
    #         upload_dict = {}
    #         if len(unique_fields) == len(kwarg.keys()):
    #             for _db_column, _value in kwarg.items():
    #                 db_column, value = __checkInputDictForCreation(_db_column, _value, unique_fields)
    #                 upload_dict[db_column] = value

    #     data_model_field_list = [
    #         {'name': field.name, 'null': field.null}
    #         for field in self.data_model._meta.get_fields()
    #     ]


    def __getGroupObject(group_id):
        try:
            return self.group_model.objects.get(id=group_id).first()
        except ObjectDoesNotExist:
            raise NotUpdatableError(
                f"{self.group_model.__name__} with id {group_id} does not exist"
            )


    def __getDataObject(group_obj, date):
        try:
            if date is None:
                data_obj = data_model.objects.filter(
                    **{self.__group_model_name: group_obj}
                ).latest('id')
            else:
                data_obj = data_model.objects.filter(
                    **{self.__group_model_name: group_obj, 'date__lte': date}
                ).latest('id')
        except ObjectDoesNotExist:
            raise NonExistentGroupError(
                f"{data_model.__name__} with group_id {group_id} does not exist at date {date}")

        return data_obj
    
    def __setManagerObjectDjangoCache(self):
        cache_key = f"{self.__class__.__name__}|{self.group_id}"
        cache.set(cache_key, self)

    def updateCache(self):
        if self.search_date is None:
            self.__setManagerObjectDjangoCache()
        CacheEntry.objects.set_cache_data(self.__class__.__name__, self.group_id, self, self.date)

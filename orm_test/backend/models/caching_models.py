from django.db import models
from django.db.models import Max, Q
import pickle, json
from datetime import datetime
from hashlib import md5

class CacheManager(models.Model):
    """
    A Django model representing cache entries, which store the manager name,
    group ID, date, and pickled data.
    """
    manager_name = models.CharField(max_length=100)
    group_id = models.IntegerField()
    date = models.DateTimeField()
    data = models.BinaryField()

    class Meta:
        unique_together = ('manager_name', 'group_id', 'date')

    @classmethod
    def get_cache_data(
        cls,
        manager_name: str,
        group_model_obj: models.Model,
        group_model_name: str,
        data_model: models.Model,
        input_group_id: int,
        date: datetime | None
    ) -> object | None:
        """
        Retrieve cached data for a given manager name, group model object,
        group model name, data model, input group ID, and date.
        
        Args:
            manager_name (str): The name of the manager.
            group_model_obj (models.Model): The group model object.
            group_model_name (str): The name of the group model.
            data_model (models.Model): The data model.
            input_group_id (int): The input group ID.
            date (datetime.datetime): The date used for filtering the cached
                data. If set to None, the latest date will be used.

        Returns:
            object: The cached data as a Python object, or None if no cache
            entry is found.
        """
        try:
            if date is None:
                latest_dates = data_model.objects.filter(
                    **{group_model_name: group_model_obj}
                ).values(group_model_name).annotate(latest_date=Max('date'))
            else:
                latest_dates = data_model.objects.filter(
                    **{'date__lt': date, group_model_name:group_model_obj}
                ).values(group_model_name).annotate(latest_date=Max('date'))

            result = cls.objects.filter(
                manager_name=manager_name,
                date=latest_dates.values('latest_date')[:1],
                group_id=input_group_id
            )
            if result.exists():
                entry = result.first()
                return pickle.loads(entry.data)
        except cls.DoesNotExist:
            pass
        except data_model.DoesNotExist:
            raise ValueError(f'data_model {data_model} is not valid')
        return None

    @classmethod
    def set_cache_data(
        cls,
        manager_name: str,
        group_id: int,
        data: object,
        date: datetime
    ) -> None:
        """
        Store data in the cache for a given manager name, group ID, data, and
        date.

        Args:
            manager_name (str): The name of the manager.
            group_id (int): The group ID.
            data (object): The data to be stored in the cache as a Python
                object.
            date (datetime.datetime): The date for the cache entry.

        Returns:
            None
        """
        entry, _ = cls.objects.get_or_create(
            manager_name=manager_name,
            group_id=group_id,
            date=date
        )
        entry.data=pickle.dumps(data)
        entry.save()


class CacheIntermediate(models.Model):
    """
    A Django model representing cache entries, which store the
    intermediate name, identification, start_date, end_date and pickled data.
    """
    intermediate_name = models.CharField(max_length=100)
    identification = models.JSONField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    data = models.BinaryField()

    class Meta:
        unique_together = (
            'intermediate_name',
            'identification',
            'start_date',
            'end_date'
        )

    @classmethod
    def get_cache_data(
        cls,
        intermediate_name: str,
        identification_dict: dict,
        date: datetime | None
    ) -> object | None:
        """
        Get cached data based on intermediate_name, identification_dict, and
        date. If date is None, use the current datetime.

        Args:
            intermediate_name (str): The intermediate name.
            identification_dict (dict): The identification dictionary.
            date (datetime | None): The datetime to filter the data.

        Returns:
            object: The cached data if found, None otherwise.
        """
        if date is None:
            date = datetime.now()
        try:
            result = cls.objects.filter(
                Q(start_date__lte=date, end_date__gte=date) | 
                Q(start_date__lte=date, end_date__isnull=True),
                intermediate_name=intermediate_name,
                identification = cls.getIdString(identification_dict),
            )
            if result.exists():
                entry = result.first()
                return pickle.loads(entry.data)
        except cls.DoesNotExist:
            pass
        return None

    @classmethod
    def set_cache_data(
        cls,
        intermediate_name: str,
        identification_dict: dict,
        data: object,
        start_date: datetime,
        end_date: datetime | None
    ) -> None:
        """
        Set cached data based on intermediate_name, identification_dict,
        start_date, end_date and data.

        Args:
            intermediate_name (str): The intermediate name.
            identification_dict (dict): The identification dictionary.
            data (object): The data to be cached.
            start_date (datetime): The start datetime of the cache data.
            end_date (datetime | None): The end datetime of the cache data.
        """
        entry, _ = cls.objects.get_or_create(
            intermediate_name=intermediate_name,
            identification=cls.getIdString(identification_dict),
            start_date=start_date,
            end_date=end_date
        )
        entry.data=pickle.dumps(data)
        entry.save()

    @staticmethod
    def getIdString(identification_dict: dict) -> str:
        """
        Convert an identification_dict into a JSON string, with keys sorted.

        Args:
            identification_dict (dict): The identification dictionary.

        Returns:
            str: The sorted JSON string of the identification dictionary.
        """
        id_json = json.dumps(identification_dict, sort_keys=True)
        return md5(id_json).hexdigest()
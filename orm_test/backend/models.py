from django.db import models
from django.db.models import Max, Subquery
import pickle


class GroupTable(models.Model):
    """
    An abstract Django model for representing group tables.
    """
    class Meta:
        abstract = True

class ReferenceTable(models.Model):
    """
    An abstract Django model for representing reference tables.
    """
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class User(ReferenceTable):
    """
    A Django model representing a User with a Microsoft ID, name, last name, email, and last login date.
    """
    microsoft_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class DataTable(models.Model):
    """
    An abstract Django model for representing data tables, including date, creator, and active status.
    """
    date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class CacheEntry(models.Model):
    """
    A Django model representing cache entries, which store the manager name, group ID, date, and pickled data.
    """
    manager_name = models.CharField(max_length=100)
    group_id = models.IntegerField()
    date = models.DateTimeField()
    data = models.BinaryField()

    class Meta:
        unique_together = ('manager_name', 'group_id', 'date')

    @classmethod
    def get_cache_data(cls, manager_name, group_model_obj, group_model_name, data_model, input_group_id, date):
        """
        Retrieve cached data for a given manager name, group model object, group model name, data model, input group ID, and date.
        
        Args:
            manager_name (str): The name of the manager.
            group_model_obj (models.Model): The group model object.
            group_model_name (str): The name of the group model.
            data_model (models.Model): The data model.
            input_group_id (int): The input group ID.
            date (datetime.datetime): The date used for filtering the cached data. If set to None, the latest date will be used.

        Returns:
            object: The cached data as a Python object, or None if no cache entry is found.
        """
        try:
            if date is None:
                latest_dates = data_model.objects.filter(
                    **{group_model_name: group_model_obj}
                ).values(group_model_name).annotate(latest_date=Max('date'))
            else:
                latest_dates = data_model.objects.filter(
                    date__lt=date,
                    group_model_name=group_model_obj
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
    def set_cache_data(cls, manager_name, group_id, data, date):
        """
        Store data in the cache for a given manager name, group ID, data, and date.

        Args:
            manager_name (str): The name of the manager.
            group_id (int): The group ID.
            data (object): The data to be stored in the cache as a Python object.
            date (datetime.datetime): The date for the cache entry.

        Returns:
            None
        """
        entry, newly_created = cls.objects.get_or_create(
            manager_name=manager_name,
            group_id=group_id,
            date=date
        )
        entry.data=pickle.dumps(data)
        entry.save()


class ProjectGroup(GroupTable):
    """
    A Django model representing a project group.
    """
    def __str__(self):
        return self.id


class Project(DataTable):
    """
    A Django model representing a project, including its name, project number, and associated project group.
    """
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProjectUserGroup(GroupTable):
    """
    A Django model representing a project user group, which associates a user with a project group.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project_group')

    def __str__(self):
        return f"{self.user} - {self.project_group}"


class ProjectUserRole(ReferenceTable):
    """
    A Django model representing a project user role, which includes a role name.
    """
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name


class ProjectUser(DataTable):
    """
    A Django model representing a project user, including their project user group and project user roles.
    """
    project_user_group = models.ForeignKey(ProjectUserGroup, on_delete=models.CASCADE)
    project_user_role = models.ManyToManyField(ProjectUserRole, blank=False)

    def __str__(self):
        return f'ProjectUser {self.id}'


class DerivativeConstelliumGroup(GroupTable):
    """
    A Django model representing a derivative Constellium group, which associates a derivative Constellium group with a project group.
    """
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class DerivativeType(ReferenceTable):
    """
    A Django model representing a derivative type, which includes a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PredictionAccuracy(ReferenceTable):
    """
    A Django model representing a prediction accuracy, which includes a name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DerivativeConstellium(DataTable):
    """
    A Django model representing a derivative Constellium, including its name, start and end dates, derivative type, estimated price, estimated weight, and prediction accuracy.
    """
    derivative_constellium_group = models.ForeignKey(DerivativeConstelliumGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sop_date = models.DateField()
    eop_date = models.DateField()
    derivative_type = models.ForeignKey(DerivativeType, on_delete=models.CASCADE)
    estimated_price = models.FloatField()
    estimated_weight = models.FloatField()
    prediction_accuracy = models.ForeignKey(PredictionAccuracy, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
from django.db import models
from django.db.models import Max, Subquery
import pickle


class GroupTable(models.Model):
    class Meta:
        abstract = True

class ReferenceTable(models.Model):
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True
class User(ReferenceTable):
    microsoft_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class DataTable(models.Model):
    date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class CacheEntry(models.Model):
    manager_name = models.CharField(max_length=100)
    group_id = models.IntegerField()
    date = models.DateTimeField()
    data = models.BinaryField()

    class Meta:
        unique_together = ('manager_name', 'group_id', 'date')

    @classmethod
    def get_cache_data(cls, manager_name, group_model_obj, group_model_name, data_model, input_group_id, date):
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
        entry, newly_created = cls.objects.get_or_create(
            manager_name=manager_name,
            group_id=group_id,
            date=date
        )
        entry.data=pickle.dumps(data)
        entry.save()


class ProjectGroup(GroupTable):

    def __str__(self):
        return self.id


class Project(DataTable):
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProjectUserGroup(GroupTable):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project_group')

    def __str__(self):
        return f"{self.user} - {self.project_group}"


class ProjectUserRole(ReferenceTable):
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name


class ProjectUser(DataTable):
    project_user_group = models.ForeignKey(ProjectUserGroup, on_delete=models.CASCADE)
    project_user_role = models.ManyToManyField(ProjectUserRole, blank=True)

    def __str__(self):
        return f'ProjectUser {self.id}'


class DerivativeConstelliumGroup(GroupTable):
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class DerivativeType(ReferenceTable):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PredictionAccuracy(ReferenceTable):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DerivativeConstellium(DataTable):
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
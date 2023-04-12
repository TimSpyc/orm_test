from django.db import models
from django.db.models import Max, Subquery
import pickle

class DerivativeConstelliumGroup(models.Model):
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class DerivativeType(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PredictionAccuracy(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DerivativeConstellium(models.Model):
    derivative_constellium_group = models.ForeignKey(DerivativeConstelliumGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sop_date = models.DateField()
    eop_date = models.DateField()
    derivative_type = models.ForeignKey(DerivativeType, on_delete=models.CASCADE)
    estimated_price = models.FloatField()
    estimated_weight = models.FloatField()
    prediction_accuracy = models.ForeignKey(PredictionAccuracy, on_delete=models.CASCADE)
    date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField()

    def __str__(self):
        return self.name


class CacheEntry(models.Model):
    manager_name = models.CharField(max_length=100)
    group_id = models.IntegerField()
    date = models.DateTimeField()
    data = models.BinaryField()

    class Meta:
        unique_together = ('manager_name', 'group_id', 'date')

    @classmethod
    def get_cache_data(cls, manager_name, data_model, group_id, date):
        try:
            if date is None:
                latest_dates = data_model.objects.filter(
                    group_id=group_id
                ).values('group_id').annotate(latest_date=Max('date'))
            else:
                latest_dates = data_model.objects.filter(
                    date__lt=date,
                    group_id=group_id
                ).values('group_id').annotate(latest_date=Max('date'))

            result = cls.objects.filter(
                manager_name=manager_name,
                date=Subquery(latest_dates.values('latest_date')[:1]),
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
        entry = cls.objects.get_or_create(
            manager_name=manager_name,
            group_id=group_id,
            date=date
        )
        entry.data=pickle.dumps(data)
        entry.save()


class User(models.Model):
    microsoft_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class ProjectGroup(models.Model):

    def __str__(self):
        return self.id

class Project(models.Model):
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=255, unique=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)
    active = models.BooleanField()

    def __str__(self):
        return self.name


class ProjectUserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project_group')

    def __str__(self):
        return f"{self.user} - {self.project_group}"


class ProjectUserRole(models.Model):
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name


class ProjectUser(models.Model):
    date = models.DateTimeField()
    project_user_group = models.ForeignKey(ProjectUserGroup, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    project_user_roles = models.ManyToManyField(ProjectUserRole, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'ProjectUser {self.id}'

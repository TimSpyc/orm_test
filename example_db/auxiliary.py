from datetime import datetime, timedelta
from faker import Faker
from django.db.models import Model
import random
import string
from backend.models import User

from backend.src.auxiliary.manager import transferToSnakeCase

fake = Faker()


def getRandomDateTime(
    t1: datetime = datetime.now(),
    t_delta_days: int = 2*365
) -> datetime:
    
    t2 = t1 - timedelta(days=t_delta_days)
    return fake.date_time_between_dates(datetime_start=t2, datetime_end=t1)


def getRandomUser():
    return User.objects.order_by('?').first()


def getRandomReference(obj: Model) -> object:
    return obj.objects.order_by('?').first()


def prevOrNewData(
    new_data: any,
    column: str,
    group_obj: Model,
    model: Model,
    chance_for_no_change: float = 0.7
) -> any:
    group_name = transferToSnakeCase(group_obj.__class__.__name__)
    if len(model.objects.all()) and model.objects.filter(**{group_name: group_obj}):
        last_entry = model.objects.filter(**{group_name: group_obj}).latest('date')

        if column == 'date' or not randomChoice(chance_for_no_change):
            return new_data
        else:
            return getattr(last_entry, column)
    else:
        return new_data


def modelCreationDict(
    data_dict: dict,
    data_model: Model,
    group_obj: Model,
    chance_for_no_change: float = 0.7
):
    new_data_dict = {}
    for key, value in data_dict.items():
        new_data_dict[key] = prevOrNewData(
            value,
            key,
            group_obj,
            data_model,
            chance_for_no_change,
        )
    return new_data_dict


def deactivateLastObjectRandomly(data_model: Model, chance_for_no_change: float = 0.7):
    if randomChoice(chance_for_no_change):
        data_model.active = 0
        data_model.save()


def randomChoice(chance_for_false):
    random_choice = random.randint(1, 100)/100
    return random_choice > chance_for_false


def randomLetters(length = 4):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def drawingNumberGenerator(drawing_type: str) -> str:
    return f'AS_{random.randint(1,99):02}_{drawing_type}_{random.randint(10000,99999):05}'
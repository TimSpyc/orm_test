# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import AbsenceGroup, Absence, User, AbsenceType

# TODO: Implement the possibility to fake a confirmation process (decorator?)
# -> Therefore the user and creator must be the same for the first data point.
# Also the is_accepted must be Null.
# -> The second data point must have the manager as creator and True or False
# as is_accepted value.

def createAbsenceGroupDict(cls):
    return {"user": cls.getRandomForeignKeyRelation(User)}

def createAbsenceDataDict(cls):
    absence_start_date = cls.getRandomDateTime()
    absence_end_date = cls.getRandomDateTime()

    while absence_end_date < absence_start_date:
        absence_end_date = cls.getRandomDateTime()

    return {
        "absence_type": cls.getRandomForeignKeyRelation(AbsenceType),
        "absence_start_date": absence_start_date,
        "absence_end_date": absence_end_date,
        "description": cls.getRandomDescription(),
        "creator": cls.group_data_dict["user"],
    }

class PopulateAbsence(GeneralPopulate):
    group_definition = (AbsenceGroup, createAbsenceGroupDict)
    data_definition = (Absence, createAbsenceDataDict)

    max_history_points = 5
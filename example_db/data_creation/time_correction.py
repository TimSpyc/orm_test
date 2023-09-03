# Responsible Maximilian Kelm
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from example_db.populate import GeneralPopulate
from backend.models import TimeCorrectionGroup, TimeCorrection, User, TimeCorrectionType

# TODO: Implement the possibility to fake a confirmation process (decorator?)
# -> Therefore the user and creator must be the same for the first data point.
# Also the is_accepted must be Null.
# -> The second data point must have the manager as creator and True or False
# as is_accepted value.

def createTimeCorrectionGroupDict(cls):
    return {"user": cls.getRandomForeignKeyRelation(User)}

def createTimeCorrectionDataDict(cls):
    # TODO: The time stamps must all be posted on the same day. In addition, 
    # the hours should be realistic.
    time_start_of_work = cls.getRandomDateTime()
    time_start_of_lunch_break = cls.getRandomDateTime()
    time_end_of_lunch_break = cls.getRandomDateTime()
    time_end_of_work = cls.getRandomDateTime()

    return {
        "time_correction_type": cls.getRandomForeignKeyRelation(TimeCorrectionType),
        "time_start_of_work": time_start_of_work,
        "time_start_of_lunch_break": time_start_of_lunch_break,
        "time_end_of_lunch_break": time_end_of_lunch_break,
        "time_end_of_work": time_end_of_work,
        "description": cls.getRandomDescription(),
    }

class PopulateTimeCorrection(GeneralPopulate):
    group_definition = (TimeCorrectionGroup, createTimeCorrectionGroupDict)
    data_definition = (TimeCorrection, createTimeCorrectionDataDict)

    max_history_points = 5
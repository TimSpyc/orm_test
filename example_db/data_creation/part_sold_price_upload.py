if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference
from backend.models import PartSoldPriceUpload, PartSoldPriceUploadGroup, PartSoldGroup

fake = Faker()

def populatePartSoldPriceUpload():
    valid_from_date = fake.date_time_between(start_date='-3y', end_date='now')
    part_sold_price_upload_group = PartSoldPriceUploadGroup(
        part_sold_group = getRandomReference(PartSoldGroup),
        valid_from = valid_from_date
    )

    part_sold_price_upload_group.save()

    part_sold_price_upload = PartSoldPriceUpload(
        part_sold_price_upload_group = part_sold_price_upload_group,
        uploaded = fake.date_time_between(start_date=valid_from_date, end_date='now'),
        price = random.uniform(1, 175.5),
        description = fake.text(),
        source = random.choice(['customer', 'calculated', 'other'])
    )

    part_sold_price_upload.save()

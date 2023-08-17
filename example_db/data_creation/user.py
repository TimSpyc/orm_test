if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from backend.models import User

fake = Faker()

def populateUser():
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f'{first_name}.{last_name}@constellium.com'

    person = User(
        microsoft_id = fake.uuid4(),
        first_name = first_name,
        last_name = last_name,
        email = email,
        last_login = random.choice([fake.date_time(), None])
    )
    person.save()
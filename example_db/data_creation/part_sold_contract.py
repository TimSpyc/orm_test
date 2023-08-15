if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from backend.models import PartSoldContract, PartSoldContractGroup

fake = Faker()

def populatePartSoldContract():
    part_sold_contract_group = PartSoldContractGroup(
        contract_number = random.randint(1000000000, 9999999999),
        contract_date = fake.date_between(start_date='-10y', end_date='today'),
    )
    part_sold_contract_group.save()

    part_sold_contract = PartSoldContract(
        part_sold_contract_group = part_sold_contract_group,
        description = fake.text(max_nb_chars=2000, ext_word_list=None),
    )
    part_sold_contract.save()

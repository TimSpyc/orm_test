if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, deactivateLastObjectRandomly, getRandomUser, getRandomDateTime, drawingNumberGenerator
from backend.models import (
    Patent,
    PatentGroup,
    PatentStatus,
    PatentTag,
    PatentClaim,
    PartGroup,
    FileGroup
)

fake = Faker()

def populatePatent():
    patent_group = PatentGroup(
        patent_number = random.choice([drawingNumberGenerator('E'), drawingNumberGenerator('Z')])
    )
    patent_group.save()

    patent = Patent(
        patent_group = patent_group,
        remark = fake.text(max_nb_chars=255),
        abstract = fake.text(max_nb_chars=255),
        priority_date = fake.date_time(),
        status = getRandomReference(PatentStatus),
        creator = getRandomUser(),
        date= getRandomDateTime(),
    )
    patent.save()

    for _ in range(random.randint(0,5)):
        patent.inventor.add(getRandomUser())
    
    for _ in range(random.randint(0,5)):
        patent.patent_tag.add(getRandomReference(PatentTag))

    for _ in range (random.randint(0,5)):
        patent.part_group.add(getRandomReference(PartGroup))
    
    for _ in range(random.randint(0,5)):
        patent.drawing.add(getRandomReference(FileGroup))
    
    patent.save()

    for i in range(random.randint(0,5)):
        patent_claim = PatentClaim(
            patent = patent,
            text = fake.ean(),
            claim_number = i+1
        )
        patent_claim.save()

    deactivateLastObjectRandomly(patent)
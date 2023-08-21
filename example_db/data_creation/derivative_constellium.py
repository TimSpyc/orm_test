if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, deactivateLastObjectRandomly, prevOrNewData, getRandomUser, getRandomDateTime
from backend.models import DerivativeConstelliumDerivativeLmcConnection, DerivativeConstellium, DerivativeConstelliumGroup, DerivativeType, PredictionAccuracy, DerivativeLmcGroup, ProjectGroup

fake = Faker()

def populateDerivativeConstelliumWithDerivativeLmcConnection():
    derivative_constellium_group = DerivativeConstelliumGroup(
        project_group = getRandomReference(ProjectGroup)
    )
    derivative_constellium_group.save()

    for _ in range(random.randint(1, 5)):
        derivative_constellium = DerivativeConstellium(**{
            "derivative_constellium_group": derivative_constellium_group,
            "name": prevOrNewData(
                fake.name(),
                "name",
                derivative_constellium_group,
                DerivativeConstellium
            ),
            "derivative_type": prevOrNewData(
                getRandomReference(DerivativeType),
                "derivative_type",
                derivative_constellium_group,
                DerivativeConstellium,
                chance_for_no_change=0.9
            ),
            "estimated_price": prevOrNewData(
                random.uniform(0, 150),
                "estimated_price",
                derivative_constellium_group,
                DerivativeConstellium
            ),
            "estimated_weight": prevOrNewData(
                random.uniform(0.25, 25),
                "estimated_weight",
                derivative_constellium_group,
                DerivativeConstellium
            ),
            "prediction_accuracy": prevOrNewData(
                getRandomReference(PredictionAccuracy),
                "prediction_accuracy",
                derivative_constellium_group,
                DerivativeConstellium
            ),
            "creator": getRandomUser(),
            "date": getRandomDateTime()
        })
        
        derivative_constellium.save()

        for _ in range(random.randint(0, 15)):
            derivative_lmc_connection = DerivativeConstelliumDerivativeLmcConnection(**{
                "derivative_constellium": derivative_constellium,
                "derivative_lmc": getRandomReference(DerivativeLmcGroup),
                "take_rate": random.uniform(0, 1),
            })
            derivative_lmc_connection.save()

    deactivateLastObjectRandomly(derivative_constellium)
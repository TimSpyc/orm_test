if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from backend.src.auxiliary import db
import random
from example_db.data_creation.reference_models import fillReferenceTables
import example_db.data_creation.user as user
import example_db.data_creation.project as project
import example_db.data_creation.derivative_lmc as derivative_lmc 
import example_db.data_creation.derivative_lmc_volume as derivative_lmc_volume

db.truncate_all_tables()

print("Start")

fillReferenceTables()

print("Done with Reference Tables")

for _ in range(random.randint(5, 500)):
    user.createFakeUser()
print("Done with Fake User")

for _ in range(random.randint(50, 200)):
    project.createFakeProjectWithHistory()

print("Done with Fake Project")
derivative_lmc.createFakeRevisionsLmc(
    start_year=2019,
    end_year=2023
)

for _ in range(random.randint(10, 50)):
    derivative_lmc.createFakeCustomer()

for _ in range(random.randint(150, 1000)):
    derivative_lmc.createFakeCustomerPlant()

for _ in range(random.randint(500, 5000)):
    derivative_lmc.createFakeDerivativeLmc()
print("Done with Fake Derivative_LMC")

derivative_lmc_volume.createVolumeForAllDerivativeLmc()
print("Done with Fake LMC Volume")

print("Database was filled with random data")
if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from backend.src.auxiliary import db
import random
import user
import project
import derivative_lmc 

db.truncate_all_tables()

print("Start")

for _ in range(random.randint(5, 500)):
    user.createFakeUser()
print("Done with Fake User")

for _ in range(random.randint(50, 2000)):
    project.createFakeProjectWithHistory()

print("Done with Fake Project")
derivative_lmc.createFakeRevisionsLmc()

for _ in range(random.randint(10, 50)):
    derivative_lmc.createFakeCustomer()

for _ in range(random.randint(150, 1000)):
    derivative_lmc.createFakeCustomerPlant()

for _ in range(random.randint(500, 5000)):
    derivative_lmc.createFakeDerivativeLmc()
print("Done with Fake Derivative_LMC")

print("Database was filled with random data")
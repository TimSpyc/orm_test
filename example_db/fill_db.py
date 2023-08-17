if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from backend.src.auxiliary.db import truncate_all_tables
import random
from example_db.data_creation import *
from auxiliary import loadingBarForPopulateScripts
from backend.src.auxiliary.string_modification import knowledgeHubLogoPrint


def run_db_filler(debug=False):
    knowledgeHubLogoPrint()
    print('''

  
        This script will fill the database with random data and truncate
        all tables before filling. Do you want to proceed? (y/n)


    ''')
    command = input()
    print()
    if command not in ['y', 'Y', 'yes', 'Yes']:
        print('aborting...')
        return 
    fill_data_function_list = [
        (1, 1, truncate_all_tables),
        (1, 1, fillReferenceTables),
        (50,500, populateUser),
        (1000, 5000, populatePartRecipient),
        (1000, 2000, populateSapNumber),
        (10, 50, populateCustomer),
        (100, 200, populateCustomerPlant),
        (5, 200, populateProjectWithHistory),
        (100, 500, populateDerivativeLmc),
        (250, 500, populateDerivativeConstelliumWithDerivativeLmcConnection),
        (10, 100, populateNorm),
        (10, 50, populateMaterialAlloyTreatment),
        (10, 50, populateMaterialAlloy),
        (10, 50, populateMaterial),
        (500, 1000, populateCrossSection),
        (1000, 5000, populatePart),
        (250, 750, populateBillOfMaterial),
        (100, 200, populatePartSoldContract),
        (200, 600, populatePartSold),
        (100, 500, populatePartSoldCustomerPrice),
        (100, 500, populatePartSoldPriceUpload),
        (100, 500, populateProjectStaffCost),
        (100, 500, populateProjectUser),
        (1, 1, populateStockExchangeData),
        (1, 1, populateVolumeForAllDerivativeLmc),
    ]

    for min_iterations, max_iterations, function in fill_data_function_list:
        if debug:
            iterations = 1
        elif max_iterations == 0:
            iterations = 0
        else:
            iterations = random.randint(min_iterations, max_iterations)
        loadingBarForPopulateScripts(
            max_iterations = iterations,
            function = function
        )

    print("Database was filled with random data")

if __name__ == '__main__':
    run_db_filler(debug=False)

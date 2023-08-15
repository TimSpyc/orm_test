if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from backend.models.reference_models import *
from datetime import date

fake = Faker()

def createCurrencies():
    currency = Currency(
        name = 'euro',
        abbreviation = 'eur',
        symbol = '€'
    )
    currency.save()

    currency = Currency(
        name = 'us-dollar',
        abbreviation = 'usd',
        symbol = '$'
    )
    currency.save()

    currency = Currency(
        name = 'pound',
        abbreviation = 'gbp',
        symbol = '£'
    )
    currency.save()

    currency = Currency(
        name = 'franc',
        abbreviation = 'chf',
        symbol = 'CHF'
    )
    currency.save()

def createNormTypes():
    norm_type = NormType(
        name = 'material'
    )
    norm_type.save()

    norm_type = NormType(
        name = 'part'
    )
    norm_type.save()

    norm_type = NormType(
        name = 'other'
    )
    norm_type.save()

def createPartTypes():
    part_type_list = [
        {"name_csg":"adapter"},
        {"name_csg":"adhesive"},
        {"name_csg":"assembly"},
        {"name_csg":"barrier"},
        {"name_csg":"baseplate"},
        {"name_csg":"battery"},
        {"name_csg":"battery enclosure"},
        {"name_csg":"bearing"},
        {"name_csg":"blind rivet"},
        {"name_csg":"blind rivet nut"},
        {"name_csg":"blind rivet stud"},
        {"name_csg":"bolt"},
        {"name_csg":"bushing"},
        {"name_csg":"cage nut"},
        {"name_csg":"camera protection"},
        {"name_csg":"crash can"},
        {"name_csg":"crash management system"},
        {"name_csg":"cross member"},
        {"name_csg":"door"},
        {"name_csg":"fascia"},
        {"name_csg":"foam"},
        {"name_csg":"frame"},
        {"name_csg":"heat sink"},
        {"name_csg":"holder"},
        {"name_csg":"joining definition"},
        {"name_csg":"locator definition"},
        {"name_csg":"longitudinal member"},
        {"name_csg":"measuring point"},
        {"name_csg":"member"},
        {"name_csg":"misc."},
        {"name_csg":"node"},
        {"name_csg":"nut"},
        {"name_csg":"nut plate"},
        {"name_csg":"package"},
        {"name_csg":"pillar"},
        {"name_csg":"pin"},
        {"name_csg":"plate"},
        {"name_csg":"press nut"},
        {"name_csg":"press stud"},
        {"name_csg":"profile"},
        {"name_csg":"punch nut"},
        {"name_csg":"reinforcement"},
        {"name_csg":"rivet"},
        {"name_csg":"seal"},
        {"name_csg":"seat cross member"},
        {"name_csg":"shaft"},
        {"name_csg":"sheet"},
        {"name_csg":"side impact beam"},
        {"name_csg":"sill"},
        {"name_csg":"spacer"},
        {"name_csg":"speed nut"},
        {"name_csg":"stopper"},
        {"name_csg":"strut"},
        {"name_csg":"sub-assembly"},
        {"name_csg":"sub-frame"},
        {"name_csg":"support"},
        {"name_csg":"surface treatment"},
        {"name_csg":"suspension part"},
        {"name_csg":"threaded insert"},
        {"name_csg":"towing eye mount"},
        {"name_csg":"towing hook"},
        {"name_csg":"tunnel"},
        {"name_csg":"wall"},
        {"name_csg":"washer"},
        {"name_csg":"welding nut"},
        {"name_csg":"welding seam"},
        {"name_csg":"welding spot"},
        {"name_csg":"welding stud"},
        {"name_csg":"wheel claw"}
    ]
    for part_type in part_type_list:
        part_type = PartType(
            name = part_type['name_csg']
        )
        part_type.save()

def createPartPositions():
    part_position_list = [
        '1lp',
        '2lp',
        '3lp',
        'front',
        'rear',
        'inner',
        'outer',
        'left',
        'right',
        'center',
    ]
    for part_position in part_position_list:
        part_position = PartPosition(
            name = part_position
        )
        part_position.save()

def createSemiFinishedProductTypes():
    semi_finished_product_type_list = [
        'profile',
        'standard_part',
        'sheet metal part - steel'
        'sheet metal part - aluminium',
        'cast part',
        'forged part',
        'plastic part',
    ]
    for semi_finished_product_type in semi_finished_product_type_list:
        semi_finished_product_type = SemiFinishedProductType(
            name = semi_finished_product_type
        )
        semi_finished_product_type.save()

def createMaterialTypes():
    material_type_list = [
        'aluminum',
        'steel',
        'polymer',
        'iron'
        'other',
    ]
    for material_type in material_type_list:
        material_type = MaterialType(
            name = material_type
        )
        material_type.save()
    
def createPartSoldPriceComponentTypes():
    part_sold_price_component_type_list = [
        'value add',
        'additional logistic',
        'material overhead',
        'energy',
        'path through',
        'product development allocation',
        'call off change',
        'spare part',
        'other',
    ]

    for part_sold_price_component_type in part_sold_price_component_type_list:
        part_sold_price_component_type = PartSoldPriceComponentType(
            name = part_sold_price_component_type
        )
        part_sold_price_component_type.save()

def createPriceUploadSources():
    price_upload_source_list = [
        'customer',
        'internal',
        'other',
    ]

    for price_upload_source in price_upload_source_list:
        price_upload_source = PriceUploadSource(
            name = price_upload_source
        )
        price_upload_source.save()

def createSavingUnits():
    saving_unit_list = [
        'currency',
        'percent',
    ]

    for saving_unit in saving_unit_list:
        saving_unit = SavingUnit(
            name = saving_unit
        )
        saving_unit.save()

def createPartSoldMaterialPriceTypes():
    part_sold_material_type_list = [
        'lme',
        'ecdp',
        'billet up charge',
        'steel',
    ]

    for part_sold_material_type in part_sold_material_type_list:
        part_sold_material_type = PartSoldMaterialPriceType(
            name = part_sold_material_type
        )
        part_sold_material_type.save()

def createDerivativeTypes():
    derivative_type_list = [
        'crash box front',
        'crash box rear',
        'crash management system front',
        'crash management system rear',
        'bumper front',
        'bumper rear',
        'side impact beam',
        'sill',
        'cross member',
        'strut',
        'body in white',
        'battery box'
    ]

    for derivative_type in derivative_type_list:
        derivative_type = DerivativeType(
            name = derivative_type
        )
        derivative_type.save()

def createPredictionAccuracies():
    prediction_accuracy_list = [
        'low (0-50%)',
        'medium (50-80%)',
        'high (80-100%)',
    ]

    for prediction_accuracy in prediction_accuracy_list:
        prediction_accuracy = PredictionAccuracy(
            name = prediction_accuracy
        )
        prediction_accuracy.save()

def createProjectUserRoles():
    project_user_role_list = [
        'program management',
        'product development',
        'sales',
        'profile procurement',
        'standard part procurement',
        'purchased part procurement',
        'process development',
        'quality',
        'logistic',
        'member'
    ]

    for project_user_role in project_user_role_list:
        project_user_role = ProjectUserRole(
            name = project_user_role
        )
        project_user_role.save()

def createFakeRevisionsLmc(start_year, end_year):
    for year in range(start_year, end_year+1):
        for month in range(1,13):
            lmc_rev = date(year, month, 1)
            RevisionLMC(revision_date = lmc_rev).save()

def createProjectStaffCostTasks():
    project_staff_cost_task_dict = {
        'development': {'description': 'Development', 'psp_element': '010'},
        'simulation': {'description': 'Simulation', 'psp_element': '020'},
        'change management': {'description': 'Change Management', 'psp_element': '030'},
        'research': {'description': 'Research', 'psp_element': '010'},
        'organization': {'description': 'Organization', 'psp_element': '010'},
        'other': {'description': 'Other work that does not fit inside the rest', 'psp_element': '010'},
    }

    for key, value in project_staff_cost_task_dict.items():
        project_staff_cost_task = ProjectStaffCostTask(
            name = key,
            description = value['description'],
            psp_element = value['psp_element']
        )
        project_staff_cost_task.save()

def fillReferenceTables():
    createCurrencies()
    createNormTypes()
    createPartTypes()
    createPartPositions()
    createSemiFinishedProductTypes()
    createMaterialTypes()
    createPartSoldPriceComponentTypes()
    createPriceUploadSources()
    createSavingUnits()
    createPartSoldMaterialPriceTypes()
    createDerivativeTypes()
    createPredictionAccuracies()
    createProjectUserRoles()
    createProjectStaffCostTasks()
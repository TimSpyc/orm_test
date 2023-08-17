if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')

    import django
    django.setup()

from faker import Faker
import random
from auxiliary import getRandomReference, deactivateLastObjectRandomly, getRandomUser, getRandomDateTime
from backend.models import BillOfMaterialGroup, BillOfMaterial, BillOfMaterialStructure, DerivativeConstelliumGroup, PartPosition, PartGroup

fake = Faker()

def populateBillOfMaterial():
    bill_of_material_group = BillOfMaterialGroup(
        derivative_constellium_group = getRandomReference(DerivativeConstelliumGroup)
    )
    bill_of_material_group.save()

    for _ in range(random.randint(1, 5)):
        start_of_production_date = fake.date_time_between(start_date='-10y', end_date='+5y', tzinfo=None)
        end_of_production_date = fake.date_time_between(start_date=start_of_production_date, end_date='+15y', tzinfo=None)
        bill_of_material = BillOfMaterial(**{
            "bill_of_material_group": bill_of_material_group,
            "start_of_production_date": start_of_production_date,
            "end_of_production_date": end_of_production_date,
            "description": fake.text(),
            "creator": getRandomUser(),
            "date": getRandomDateTime()
        })

        bill_of_material.save()
        bom_structure_element_list = []
        amount_of_bom_elements = random.choice([random.randint(1, 75), random.randint(1, 10), random.randint(1, 20)])
        for _ in range(amount_of_bom_elements):
            bill_of_material_structure = BillOfMaterialStructure(**{
                "bill_of_material": bill_of_material,
                "part_group": getRandomReference(PartGroup),
                "cumulated_quantity": random.uniform(0, 100),
            })
            bill_of_material_structure.save()

            for _ in range(random.randint(1, 5)):
                bill_of_material_structure.part_position.add(getRandomReference(PartPosition))
            bill_of_material_structure.save()
            bom_structure_element_list.append(bill_of_material_structure)
        
        nested_list = nested_set_from_list(
            bom_structure_element_list,
            max_depth=random.randint(2, 6),
            max_children=random.randint(3, 10)
        )

        for element in nested_list:
            bom_structure_element = element["value"]
            bom_structure_element.left_value_product_development = element["left"]
            bom_structure_element.right_value_product_development = element["right"]
            bom_structure_element.save()

        deactivateLastObjectRandomly(bill_of_material)
        
def nested_set_from_list(data, max_depth=3, max_children=3):
    nodes = []
    
    def build_tree(parent_left, data, depth):
        if depth > max_depth or not data:
            return parent_left
        num_children = random.randint(1, min(max_children, len(data)))
        
        for _ in range(num_children):
            if not data:
                break
            index = random.randint(0, len(data) - 1)
            value = data.pop(index)
            
            node = {"left": parent_left + 1, "value": value, "right": None}
            nodes.append(node)
            node_right = build_tree(node["left"], data, depth + (random.randint(0, 1)))
            node["right"] = node_right + 1
            parent_left = node["right"]

        return parent_left

    build_tree(0, data, 1)
    return nodes
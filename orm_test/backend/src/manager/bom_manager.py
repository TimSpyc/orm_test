from django.db import models
from backend.models import GroupTable, DataTable, DataExtensionTable, PartGroup, DerivativeConstelliumGroup, PartPosition
from backend.src.auxiliary.manager import GeneralManager

class BillOfMaterialGroup(GroupTable):
    derivative_constellium_group = models.ForeignKey(DerivativeConstelliumGroup, on_delete= models.DO_NOTHING)

    def manager(self, search_date, use_cache):
        return BillOfMaterialManager(self.id, search_date, use_cache)
    
    def __str__(self):
        return f"BillOfMaterialGroup {self.derivative_constellium_group}"

class BillOfMaterial(DataTable):
    bill_of_material_group = models.ForeignKey(BillOfMaterialGroup, on_delete= models.DO_NOTHING)
    start_of_production_date = models.DateTimeField(null=True, default=None)
    end_of_production_date = models.DateTimeField(null=True, default=None)
    description = models.CharField(max_length=255)

    @property
    def group(self):
        return self.bill_of_material_group
    
    def __str__(self):
        return f"BillOfMaterial {self.bill_of_material_group}-{self.description}"


class BillOfMaterialStructure(DataExtensionTable):
    bill_of_material = models.ForeignKey(BillOfMaterial, on_delete= models.DO_NOTHING)
    part_group = models.ForeignKey(PartGroup, on_delete= models.DO_NOTHING)
    part_position = models.ManyToManyField(PartPosition, blank=True)
    part_rate = models.FloatField()
    left_value_product_development = models.FloatField()
    right_value_product_development = models.FloatField()
    left_value_process_development = models.FloatField()
    right_value_process_development = models.FloatField()


class BillOfMaterialManager(GeneralManager):
    group_model = BillOfMaterialGroup
    data_model = BillOfMaterial
    data_extension_model_list = [BillOfMaterialStructure]

    def __init__(self, bill_of_material_group_id, search_date=None, use_cache=True):
        super().__init__(group_id=bill_of_material_group_id, search_date=search_date, use_cache=use_cache)




    @staticmethod
    def formatBillOfMaterialPositionStructureToNestedSet(
        bill_of_material_dict: list
    ) -> dict:
        pass

    @staticmethod
    def formatNestedSetToBillOfMaterialPositionStructure(
        nested_set_dict: dict
    ) -> list:
        pass



# def calculate_nested_set(input_data):
#     # Sortieren der Daten basierend auf den Positionswerten
#     sorted_input = sorted(input_data, key=lambda x: [int(i) for i in x['pos'].split('.')])
    
#     # Initialisierung der Ausgangsdaten und der Liste der offenen Knoten
#     output_data = []
#     open_nodes = []
#     group_index = {}

#     # Durchlaufen der sortierten Eingabedaten
#     for node in sorted_input:
#         left = len(output_data) * 2 + 1
        
#         # Schließen von offenen Knoten, wenn möglich
#         while open_nodes and not node['pos'].startswith(open_nodes[-1]['pos'] + '.'):
#             output_data[group_index[open_nodes[-1]['group_id']]]['right'] = len(output_data) * 2
#             open_nodes.pop()

#         # Füge den aktuellen Knoten hinzu und markiere ihn als offen
#         output_data.append({'group_id': node['group_id'], 'left': left})
#         group_index[node['group_id']] = len(output_data) - 1
#         open_nodes.append({'group_id': node['group_id'], 'pos': node['pos']})

#     # Schließen aller verbleibenden offenen Knoten
#     while open_nodes:
#         output_data[group_index[open_nodes[-1]['group_id']]]['right'] = len(output_data) * 2
#         open_nodes.pop()

#     return output_data

# input_data = [{'pos': '1', 'group_id': 1}, {'pos': '1.1', 'group_id': 2}, {'pos': '1.2', 'group_id': 3}, {'pos': '1.1.1', 'group_id': 4}]
# output_data = calculate_nested_set(input_data)
# print(output_data)

# def calculate_positions(output_data):
#     # Initialisierung der Eingabedaten und der offenen Intervalle
#     input_data = []
#     open_intervals = []

#     # Sortieren der Ausgabedaten basierend auf den linken Werten
#     sorted_output = sorted(output_data, key=lambda x: x['left'])

#     # Durchlaufen der sortierten Ausgabedaten
#     for node in sorted_output:
#         # Schließen von offenen Intervallen, wenn möglich
#         while open_intervals and not (open_intervals[-1]['left'] < node['left'] < open_intervals[-1]['right']):
#             open_intervals.pop()

#         # Füge den aktuellen Knoten hinzu und markiere das Intervall als offen
#         pos = '.'.join([str(interval['pos']) for interval in open_intervals] + [str(node['left'])])
#         input_data.append({'pos': pos, 'group_id': node['group_id']})
#         open_intervals.append({'left': node['left'], 'right': node['right'], 'pos': node['left']})

#     return input_data

# output_data = [{'group_id': 1, 'left': 1, 'right': 10}, {'group_id': 2, 'left': 2, 'right': 7}, {'group_id': 3, 'left': 8, 'right': 9}, {'group_id': 4, 'left': 3, 'right': 4}]
# input_data = calculate_positions(output_data)
# print(input_data)
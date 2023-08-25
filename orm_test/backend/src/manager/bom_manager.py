from django.db import models
from backend.models import GroupTable, DataTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager

class BillOfMaterialGroup(GroupTable):
    derivative_constellium_group = models.ForeignKey('DerivativeConstelliumGroup', on_delete= models.DO_NOTHING)

    @property
    def manager(self):
        return BillOfMaterialManager
    
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
    part_group = models.ForeignKey('PartGroup', on_delete= models.DO_NOTHING)
    part_position = models.ManyToManyField('PartPosition', blank=True)
    cumulated_quantity = models.FloatField()
    left_value_product_development = models.FloatField(null=True)
    right_value_product_development = models.FloatField(null=True)
    left_value_process_development = models.FloatField(null=True)
    right_value_process_development = models.FloatField(null=True)
    left_value_logistics = models.FloatField(null=True)
    right_value_logistics = models.FloatField(null=True)

    @property
    def data_object(self):
        return self.BillOfMaterial


class BillOfMaterialManager(GeneralManager):
    group_model = BillOfMaterialGroup
    data_model = BillOfMaterial
    data_extension_model_list = []

    def __init__(
        self,
        group_id,
        search_date=None,
        use_cache=True
    ):
        super().__init__(
            group_id=group_id,
            search_date=search_date,
            use_cache=use_cache
        )

        self.product_development_bom = self.getBillOfMaterialStructure('pd')
        self.process_development_bom = self.getBillOfMaterialStructure('ai')
        self.logistics_bom = self.getBillOfMaterialStructure('lg')

        self.updateCache()

    def getBillOfMaterialStructure(
        self,
        bom_type: str,
    ):
        head_node = self.__getHeadNode()
        key_tuple = self.__selectBomType(bom_type)
        bill_of_material_structure = self.__getBillOfMaterialStructure(
            head_node,
            key_tuple
        )
        return bill_of_material_structure

    def getBillOfMaterialDetails(
        self,
        bom_type: str,
        head_part_group_id: int | None = None
    ) -> dict:
        key_tuple = self.__selectBomType(bom_type)
        head_node = self.__getHeadNode(head_part_group_id)
        direct_child_node_list = self.__getChildNodeList(
            head_node,
            key_tuple,
            must_be_direct_child=True
        )
        leaf_node_list = self.__getChildNodeList(
            head_node,
            key_tuple,
            must_be_leaf=True
        )
        bill_of_material_structure = self.__getBillOfMaterialStructure(
            head_node,
            key_tuple
        )

        bill_of_material_detail_dict = {
            'head_node': head_node,
            'direct_child_node_list': direct_child_node_list,
            'leaf_node_list': leaf_node_list,
            'structure': bill_of_material_structure
        }
        
        return bill_of_material_detail_dict

    def __selectBomType(self, bom_type: str) -> tuple:
        bom_type_dict = {
            'pd': 'product_development',
            'ai': 'process_development',
            'lg': 'logistics'
        }
        if bom_type not in bom_type_dict.keys():
            raise ValueError(f"""
                Bill of material type {bom_type} is not supported.
            """)
        
        left_value = f"left_value_{bom_type_dict[bom_type]}"
        right_value = f"right_value_{bom_type_dict[bom_type]}"

        return left_value, right_value

    def __getHeadNode(self, head_part_group_id: int | None) -> dict:
        if head_part_group_id is None:
            return filter(
                lambda dict_data: (
                    dict_data['left_value_product_development'] == 1
                ),
                self.bill_of_material_structure_dict_list
            )
        else:
            return filter(
                lambda dict_data: (
                    dict_data['part_group'].id == head_part_group_id
                ),
                self.bill_of_material_structure_dict_list
            )

    def __getChildNodeList(
        self,
        head_node: dict,
        key_tuple: tuple,
        must_be_leaf: bool = False, 
        must_be_direct_child: bool = False
    ) -> list:
        left_value, right_value = key_tuple
        node_list = []
        for node in self.bill_of_material_structure_dict_list:
            left_node_value = node[left_value] if not None else 0
            right_node_value = node[right_value] if not None else 0
            
            head_node_left_value: head_node[left_value] if not None else 0
            head_node_right_value: head_node[right_value] if not None else 0

            is_inside = self.__checkIfIsInside(
                head_node_left_value,
                head_node_right_value,
                left_node_value,
                right_node_value
            )
            if not is_inside:
                continue

            is_leaf = self.__checkIfIsLeafNode(
                left_node_value,
                right_node_value
            )
            is_direct_child = self.__checkIfIsDirectChildNode(
                self.bill_of_material_structure_dict_list,
                head_node_left_value,
                head_node_right_value,
                left_node_value,
                right_node_value
            )
            if (
                (not must_be_leaf or is_leaf) and
                (not must_be_direct_child or is_direct_child)
            ):
                node_list.append({
                    **node,
                    'left': node[left_value],
                    'right': node[right_value],
                    'relative_quantity': (
                        node['cumulated_quantity'] /
                        head_node['cumulated_quantity']
                    ),
                })
        return node_list

    @staticmethod
    def __checkIfIsInside(
        head_node_left_value: int,
        head_node_right_value: int,
        left_node_value: int,
        right_node_value: int
    ) -> bool:
        return (
                left_node_value > head_node_left_value and
                right_node_value < head_node_right_value
            )

    @staticmethod
    def __checkIfIsDirectChildNode(
        all_node_list,
        head_node_left_value: int,
        head_node_right_value: int,
        left_node_value: int,
        right_node_value: int
    ):
        for node in all_node_list:
            is_greater_than_own_node = (
                node['left'] < left_node_value and
                node['right'] > right_node_value
            )
            is_smaller_than_head_node = (
                node['left'] > head_node_left_value and
                node['right'] < head_node_right_value
            )
            if is_greater_than_own_node and is_smaller_than_head_node:
                return False
        return True

    @staticmethod
    def __checkIfIsLeafNode(left_node_value, right_node_value):
        return left_node_value +1 == right_node_value

    def __getBillOfMaterialStructure(
        self,
        head_node: dict,
        key_tuple: tuple
    ) -> list:
        relevant_node_list = self.__getChildNodeList(
            head_node,
            key_tuple,
        )
        relevant_node_list = self.__addHeadNodeToRelevantNodeList(
            head_node,
            key_tuple,
            relevant_node_list
        )
        return self.formatNestedSetToBillOfMaterialPositionStructure(
            relevant_node_list
        )

    def __addHeadNodeToRelevantNodeList(
        self,
        head_node: dict,
        key_tuple: tuple,
        relevant_node_list: list
    ) -> list:
        left_value, right_value = key_tuple
        head_node_dict = {
            **head_node,
            'left': head_node[left_value],
            'right': head_node[right_value],
            'relative_quantity': 1
        }
        return [*relevant_node_list, head_node_dict]

    @staticmethod
    def formatBillOfMaterialPositionStructureToNestedSet(
        bill_of_material_dict: list
    ) -> list:
        #TODO: Noch nicht bugfrei!
        output_data = []
        open_nodes = []
        group_index = {}

        #sort data based on position values
        sorted_input = sorted(bill_of_material_dict, key=lambda x: [int(i) for i in x['pos'].split('.')])

        for node in sorted_input:
            left = len(output_data) * 2 + 1
            # close open nodes if possible
            while open_nodes and not node['pos'].startswith(open_nodes[-1]['pos'] + '.'):
                output_data[group_index[open_nodes[-1]['group_id']]]['right'] = len(output_data) * 2
                open_nodes.pop()

            # add the current node and mark it as open
            output_data.append({'group_id': node['group_id'], 'left': left})
            group_index[node['group_id']] = len(output_data) - 1
            open_nodes.append({'group_id': node['group_id'], 'pos': node['pos']})

        # close all remaining open nodes
        while open_nodes:
            output_data[group_index[open_nodes[-1]['group_id']]]['right'] = len(output_data) * 2
            open_nodes.pop()

        return output_data

    @staticmethod
    def formatNestedSetToBillOfMaterialPositionStructure(
        nested_set_dict: dict
    ) -> list:
        #TODO: Noch nicht bugfrei!
        bom_structure_dict = []
        open_intervals = []

        #sort the output data based on the left values
        sorted_output = sorted(nested_set_dict, key=lambda x: x['left'])

        for node in sorted_output:
            #close open intervals if possible
            while open_intervals and not (open_intervals[-1]['left'] < node['left'] < open_intervals[-1]['right']):
                open_intervals.pop()

            #add the current node and mark the interval as open
            pos = '.'.join([str(interval['pos']) for interval in open_intervals] + [str(node['left'])])
            bom_structure_dict.append({'pos': pos, 'data': node})
            open_intervals.append({'left': node['left'], 'right': node['right'], 'pos': node['left']})

        return bom_structure_dict

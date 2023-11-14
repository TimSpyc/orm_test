from django.db import models
from backend.models import GroupTable, DataTable, DataExtensionTable
from backend.src.auxiliary.manager import GeneralManager

class BillOfMaterialGroup(GroupTable):
    derivative_constellium_group = models.ForeignKey(
        'DerivativeConstelliumGroup',
          on_delete= models.DO_NOTHING
          )

    @property
    def manager(self):
        return BillOfMaterialManager
    
    def __str__(self):
        return f"BillOfMaterialGroup {
            self.derivative_constellium_group
            }"


class BillOfMaterial(DataTable):
    bill_of_material_group = models.ForeignKey(
        BillOfMaterialGroup,
          on_delete= models.DO_NOTHING
          )
    start_of_production_date = models.DateTimeField(null=True, default=None)
    end_of_production_date = models.DateTimeField(null=True, default=None)
    description = models.CharField(max_length=255)

    @property
    def group_object(self):
        return self.bill_of_material_group
    
    def __str__(self):
        return f"BillOfMaterial {
            self.bill_of_material_group}-{self.description}"


class BillOfMaterialStructure(DataExtensionTable):
    bill_of_material = models.ForeignKey(
        BillOfMaterial,
          on_delete= models.DO_NOTHING
          )
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
        return self.bill_of_material


class BillOfMaterialManager(GeneralManager):
    group_model = BillOfMaterialGroup
    data_model = BillOfMaterial
    data_extension_model_list = [BillOfMaterialStructure]

    def __init__(
        self,
        group_id,
        search_date=None,
    ):
        super().__init__(
            group_id=group_id,
            search_date=search_date,
        )

        self.product_development_bom = self.getBillOfMaterialStructure('pd')
        self.process_development_bom = self.getBillOfMaterialStructure('ai')
        self.logistics_bom = self.getBillOfMaterialStructure('lg')

        self.updateCache()

    @property
    def head_node_list(self):
        key_tuple = self.__selectBomType('pd')
        return self.__getHeadNodeList(key_tuple)
        
    def getBillOfMaterialStructure(
        self,
        bom_type: str,
        head_part_group_id: int | None = None,
    ) -> list:
        """
        Retrieve the bill of material structure based on the specified 
        BOM type and optional head part group ID.

        Args:
            bom_type (str): The type of bill of material
            head_part_group_id (int, optional): 
                The ID of the head part group. Defaults to None.

        Returns:
            list: A list containing the bill of material structure.
        """
        total_bill_of_material_structure = []
        key_tuple = self.__selectBomType(bom_type)

        head_node_list = self.__getHeadNodeList(
            head_part_group_id,
              key_tuple = key_tuple
              )
        for head_node in head_node_list:
            bill_of_material_structure = self.__getBillOfMaterialStructure(
                head_node,
                key_tuple
            )
            total_bill_of_material_structure += bill_of_material_structure
        return total_bill_of_material_structure

    def getBillOfMaterialDetails(
        self,
        bom_type: str,
        head_part_group_id: int | None = None
    ) -> list[dict]:
        """
        Retrieves details of the Bill of Material based on the specified 
        BOM type and optional head part group ID.

        Args:
            bom_type (str): 
                The type of Bill of Material to retrieve details for.
            head_part_group_id (int | None, optional): 
                The group ID of the head part. Default = None.

        Returns:
            list[dict]: 
                A list of dictionaries with details of the Bill of Material.
                Each dictionary includes information about the head node,
                direct child nodes, leaf nodes, and the hierarchical structure.
        Raises:
            ValueError: 
                If an invalid BOM type is provided or an empty 
                head part group ID is given.
        """
        key_tuple = self.__selectBomType(bom_type)
        head_node_list = self.__getHeadNodeList(head_part_group_id, key_tuple)
        bill_of_material_detail_dict_list = []

        for head_node in head_node_list:
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

            bill_of_material_detail_dict_list.append({
                'head_node': head_node,
                'direct_child_node_list': direct_child_node_list,
                'leaf_node_list': leaf_node_list,
                'structure': bill_of_material_structure
            })
        
        return bill_of_material_detail_dict_list

    def __selectBomType(self, bom_type: str) -> tuple:
        """
        Selects the left and right values corresponding to a given bom type.

        Args:
            bom_type (str): The Bill of Material type 
                -'pd' for product_development, 
                -'ai' for process_development, 
                -'lg' for logistics).

        Returns:
            tuple: A tuple containing the left and right value keys 
                for the specified BOM type.
        """
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
    

    def __getHeadNodeList(
            self, 
            head_part_group_id: int | None, 
            key_tuple: tuple[str, str]
            ) -> list[dict]:
        """
        Gets the head node dictionary for a given head part group ID.

        Args:
            head_part_group_id (int | None): 
                The ID of the head part group or None.

        Returns:
            dict: The head node dictionary that matches the specified 
                head part group ID, if None for head part group ID then
                get the first head node dictionary.
        """
        if head_part_group_id is None:
            return self.__getNodeHeadNodeList(key_tuple)
        else:
            existing_id = list(filter(
                    lambda dict_data: (
                        dict_data['part_group']['id'] == head_part_group_id
                    ),
                    self.bill_of_material_structure_dict_list
                ))
            if not existing_id:
                raise ValueError(
                    f"""
                    The head_part_group_id {head_part_group_id} 
                    does not exist.
                    """
                    )
         
        return existing_id

    def __getNodeHeadNodeList(self, key_tuple: tuple[str, str]) -> list[dict]:
        """
        Gets the head node dictionaries from a list of nodes.

        Args:
            node_list (list[dict]): List of dictionaries representing nodes.

        Returns:
            list[dict]: List of dictionaries that are head nodes.
        """
        left_value, right_value = key_tuple
        head_nodes = []
        open_ranges = []
        for node in self.bill_of_material_structure_dict_list:

            left = node.get(left_value)
            right = node.get(right_value)

            if left is not None and right is not None:
                is_head = True
                for range_data in open_ranges:
                    if left > range_data[left_value] and \
                        right < range_data[right_value]:
                        is_head = False
                        break
                if is_head:
                    head_nodes.append(node)
                open_ranges.append({left_value: left, right_value: right})

        return head_nodes
    

    def __getChildNodeList(
        self,
        head_node: dict,
        key_tuple: tuple,
        must_be_leaf: bool = False, 
        must_be_direct_child: bool = False
    ) -> list:
        """
        Creates a list of child nodes for a given node in the Bill of Material.

        Args:
            head_node (dict): 
                The parent node for which child nodes should be found.
            key_tuple (tuple): 
                A tuple of keys representing the 'left' and 'right' values
                in the nodes.
            must_be_leaf (bool, optional): If True, only leaf nodes are 
                included in the result. Default is False.
            must_be_direct_child (bool, optional): If True, only direct 
                child nodes are included in the result. Default is False.

        Returns:
            list: A list of child nodes.
        """
        
        left_value, right_value = key_tuple
        node_list = []
        found_direct_child = False
        for node in self.bill_of_material_structure_dict_list:

            left_node_value = node[left_value] if left_value in node else 0
            right_node_value = node[right_value] if right_value in node else 0

            head_node_left_value = head_node.get(left_value, 0)
            head_node_right_value = head_node.get(right_value, 0)

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
            if (
                (not must_be_leaf or is_leaf) and
                (not must_be_direct_child or not found_direct_child)
            ):
                
                is_direct_child = self.__checkIfIsDirectChildNode(
                    self.bill_of_material_structure_dict_list,
                    head_node_left_value,
                    head_node_right_value,
                    left_node_value,
                    right_node_value
                )
                if is_direct_child:
                    found_direct_child = True
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
        """
        Checks if a node is inside another node's left and right values.

        Args:
            head_node_left_value (int): The left value of the head node.
            head_node_right_value (int): The right value of the head node.
            left_node_value (int): The left value of the node to check.
            right_node_value (int): The right value of the node to check.

        Returns:
            bool: True if the node is inside the head node, otherwise False.
        """
        return (
                left_node_value > head_node_left_value and
                right_node_value < head_node_right_value
            )

    @staticmethod
    def __checkIfIsDirectChildNode(
        all_node_list: list,
        head_node_left_value: int,
        head_node_right_value: int,
        left_node_value: int,
        right_node_value: int
    )-> bool:
        """
        Checks if a node is a direct child node of another node
        in a list of nodes.

        Args:
            all_node_list (list): The list of nodes to check within.
            head_node_left_value (int): The left value of the head node.
            head_node_right_value (int): The right value of the head node.
            left_node_value (int): The left value of the node to check.
            right_node_value (int): The right value of the node to check.

        Returns:
            bool: True if the node is a direct child node, otherwise False.
        """
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
    def __checkIfIsLeafNode(
        left_node_value: int, 
        right_node_value: int
        ) -> bool:
        """
        Checks if a node is a leaf node by verifying if the 
        left value is one less than the right value.

        Args:
            left_node_value: The left value of the node.
            right_node_value: The right value of the node.

        Returns:
            bool: True if the node is a leaf node, otherwise False.
        """
        return left_node_value +1 == right_node_value

    def __getBillOfMaterialStructure(
        self,
        head_node: dict,
        key_tuple: tuple
    ) -> list:
        """
        Generates a Bill of Material structure based on a given 
        head node and key tuple.

        Args:
            head_node (dict): 
                The head node for which the structure is generated.
            key_tuple (tuple): 
                A tuple containing the left and right key names.

        Returns:
            list: A list of dictionaries representing the 
                hierarchical Bill of Material structure.
        """
        relevant_node_list = self.__getChildNodeList(
            head_node,
            key_tuple,
        )
        relevant_node_list = self.__addHeadNodeToRelevantNodeList( 
            head_node,
            key_tuple,
            relevant_node_list
        )
        return self.formatBillOfMaterialNestedSetToPositionStructure(
            relevant_node_list
        )

    def __addHeadNodeToRelevantNodeList(
        self,
        head_node: dict,
        key_tuple: tuple,
        relevant_node_list: list
    ) -> list:
        """
        Adds a head node to a list of relevant nodes with specific 
        key tuple values.

        Args:
            head_node (dict): The head node dictionary to add.
            key_tuple (tuple): A tuple containing left and right key names.
            relevant_node_list (list): The list of relevant nodes.

        Returns:
            list: The updated list of relevant nodes with the head node added.
        """
        left_value, right_value = key_tuple
        head_node_dict = {
            **head_node,
            'left': head_node[left_value],
            'right': head_node[right_value],
            'relative_quantity': 1
        }
        return [*relevant_node_list, head_node_dict]



##Nested Set
    @staticmethod
    def _checkBillOfMaterialPositionStructure(
        bill_of_material_dict: list[dict]
        ) -> None:
        """
        Checks the validity of a bill of material represented 
        in a position structure.

        Args:
            bill_of_material_dict (list[dict]): 
                List of dictionaries in a position structure.

        Raises:
            ValueError: If the input is empty, not a list or dictionary,
                or has missing key 'pos' and 'group_id' keys.
        """
        if bill_of_material_dict == []:

            raise ValueError("bill_of_material_dict cannot be empty.")
        
        if not isinstance(bill_of_material_dict, list) \
                and not isinstance(bill_of_material_dict, dict):
            
            raise ValueError("Please provide a list of dictionaries.")

        for item in bill_of_material_dict:
            if 'pos' not in item or 'group_id' not in item:

                raise ValueError(
                    f"""
                    "Invalid input format. Expected a list of dictionaries 
                    with 'pos' and 'group_id'."
                    """
                    )

    @staticmethod
    def _sortPositionStructure(bill_of_material_dict: list[dict])-> list[dict]:
        """
        Sorts a list of dictionaries representing a bill of material 
        in a position structure.

        Args:
            bill_of_material_dict (list[dict]): 
                List of dictionaries in the position structure.

        Returns:
            list[dict]: Sorted list of dictionaries.
        """
        sorted_input = sorted(
            bill_of_material_dict, 
            key=lambda x: [int(i) for i in x['pos'].split('.')]
            )
        return sorted_input
    
    @staticmethod
    def _headCheckOfBillOfMaterialPositionStructure(
        bill_of_material_dict: list[dict]
        )-> list[dict]:
        """
        A head check of a bill of material represented in a position structure.

        Args:
            bill_of_material_dict (list[dict]): 
                List of dictionaries representing the position structure.
        Raises:
            ValueError: If the hierarchy is violated.

        Returns:
            list[dict]: Formatted list of dictionaries after head check.
        """
        bill_of_material_dict = BillOfMaterialManager._sortPositionStructure(
            bill_of_material_dict
            )
        formatted_output = []
        seen_positions = set()

        for item in bill_of_material_dict:
            pos = item['pos']
            pos_parts = pos.split('.')

            if len(pos_parts) > 1:    
                parent_pos = '.'.join(pos_parts[:-1])     
                if parent_pos not in seen_positions:   
                    raise ValueError(
                        f"""
                        Invalid hierarchy at position: {pos}, 
                        parent_pos is missing: {parent_pos}
                        """
                        )

            seen_positions.add(str(pos)) 
            formatted_output.append(item)

        return formatted_output

    @staticmethod
    def formatBillOfMaterialPositionStructureToNestedSet(
        bill_of_material_list_dict: list[dict]
    ) -> list[dict]:
        """
        Converts a bill of material from a position structure 
        to a nested set structure.

        Args:
            bill_of_material_list_dict (list[dict]): 
                List of dictionaries representing the position structure.

        Returns:
            list[dict]: List of dictionaries in the nested set structure.
        """    
        BillOfMaterialManager._checkBillOfMaterialPositionStructure(
            bill_of_material_list_dict
            )
        sorted_and_validated_input = BillOfMaterialManager.\
            _headCheckOfBillOfMaterialPositionStructure(
            bill_of_material_list_dict
            )
        return BillOfMaterialManager._createNestedSet(
            sorted_and_validated_input
            )

    @staticmethod
    def _createNestedSet(
        sorted_bill_of_material_list_dict: list[dict]
        ) -> list:
        """
        Creates a nested set structure from a sorted list of 
        dictionaries from a position structure.

        Args:
            sorted_bill_of_material_list_dict (list[dict]): 
                Sorted list of dictionaries representing the bill of
                material list in a position structure.

        Returns:
            list[dict]: 
                List of dictionaries representing the nested set structure.
        """
        output_data = []
        open_nodes = []
        group_index = {}
        right_counter = 1

        for node in sorted_bill_of_material_list_dict:
            pos = node['pos']

            while open_nodes and not pos.startswith(
                open_nodes[-1]['pos'] + '.'
                ):
                output_data[group_index[open_nodes[-1]['group_id']]]['right'] \
                         = right_counter
                
                open_node = open_nodes.pop()
                open_node['right'] = right_counter
                right_counter += 1

            left = right_counter    
            right_counter += 1
 
            output_data.append({  
                'group_id': node['group_id'],
                'left': left,
                'right': None
            })
            group_index[node['group_id']] = len(output_data) - 1

            open_nodes.append({'group_id': node['group_id'], 'pos': pos})

        while open_nodes:
            output_data[group_index[open_nodes[-1]['group_id']]]['right'] \
                    = right_counter
            
            open_node = open_nodes.pop()
            open_node['right'] = right_counter
            right_counter += 1

        return output_data

        

#Position Structure
    @staticmethod
    def _checkBillOfMaterialNestedSet(
        bill_of_material_dict: list[dict]
        )-> None:
        """
        Check of a bill of material represented in a nested set structure.

        Args:
            bill_of_material_dict (list[dict]): 
                List of dictionaries representing the nested set structure.

        Raises:
            ValueError: If the input is empty, not a list or dictionary,
                 or has missing keys 'group_id', 'left' and 'right'.
        """
        if bill_of_material_dict == []:

            raise ValueError("bill_of_material_dict cannot be empty.")
        
        if not isinstance(bill_of_material_dict, list) \
                and not isinstance(bill_of_material_dict, dict):
            
            raise ValueError("Please provide a list of dictionaries.")

        for item in bill_of_material_dict:
            if not all(key in item for key in ['group_id', 'left', 'right']):

                raise ValueError(
                    f"""
                    "Invalid input format. Expected a list of dictionaries 
                     with 'group_id','left'and 'right'.")
                     """
                     )
   
    @staticmethod
    def _checkValuesBillOfMaterialNestedSet(
        bill_of_material_dict: list[dict]
        ) -> list[dict]:
        """
        Checks the values within a bill of material nested set structure 
        for validity.

        Args:
            bill_of_material_dict (list[dict]): 
                List of dictionaries representing the nested set structure.

        Raises:
            ValueError: If left value is greater than or equal to right value, 
                        if duplicate left or right values exist,
                        or if the nested set structure is violated.
        """
        left_values = set()
        right_values = set()
        stack = []

        for node in bill_of_material_dict:
            left = node['left']
            right = node['right']

            if left >= right:
                raise ValueError(
                    "left value cannot be greater than or equal to right value"
                    )
           
            if left in left_values or right in right_values:
                raise ValueError("duplicate left or right value")

            left_values.add(left)
            right_values.add(right)

            while stack and stack[-1]['right'] < right:
                stack.pop()

            if stack and left <= stack[-1]['left']:
                raise ValueError("nested set structure violated")

            stack.append(node)

        offset = min(left_values) -1
        if min(left_values) - offset != 1 or max(right_values) - offset \
            != len(bill_of_material_dict) * 2:
            raise ValueError("invalid root set")
        
        sorted_output = BillOfMaterialManager._sortNestedSet(
            bill_of_material_dict
            )
        return sorted_output

    @staticmethod
    def _sortNestedSet(bill_of_material_dict: list[dict])-> list[dict]:
        """
        Sorts a list of dictionaries in a nested set structure.

        Args:
            bill_of_material_dict (list[dict]): 
                List of dictionaries in a nested set structure.

        Returns:
            list[dict]: Sorted list of dictionaries.
        """
        sorted_output = sorted(bill_of_material_dict, key=lambda x: x['left'])
        return sorted_output
    
    @staticmethod
    def formatBillOfMaterialNestedSetToPositionStructure(
            bill_of_material_list_dict: list[dict]
        ) -> list[dict]:
        """
        Converts a nested set structure to a position structure.

        Args:
            bill_of_material_list_dict (list[dict]): 
                List of dictionaries representing the nested set structure.

        Returns:
            list[dict]: 
                List of dictionaries in the position structure.
        """    
        BillOfMaterialManager._checkBillOfMaterialNestedSet(
            bill_of_material_list_dict
            )
        validated_input = BillOfMaterialManager.\
            _checkValuesBillOfMaterialNestedSet(
            bill_of_material_list_dict
            )
        return BillOfMaterialManager._createPositionStructure(
            validated_input
            )

        
        
    @staticmethod
    def _createPositionStructure(nested_set_data: list) -> list:
        """
        Creates a position structure from a list represented 
        in a nested set structure.

        Args:
            nested_set_data (list[dict]): 
                List of dictionaries representing the nested set structure.

        Returns:
            list[dict]: List of dictionaries representing the 
                hierarchical position structure.
        """
        sorted_output = BillOfMaterialManager._sortNestedSet(nested_set_data)
        bom_structure_dict = []
        hierarchy = []
        current_pos = {}

        for node in sorted_output:
            group_id = node['group_id']
            left = node['left']
            right = node['right']

            hierarchy = BillOfMaterialManager._updateHierarchy(hierarchy, left)

            parent_pos = "" if not hierarchy else hierarchy[-1]['pos']
            current_pos = BillOfMaterialManager._updateCurrentPosition(current_pos, parent_pos)

            pos = f"{parent_pos}.{current_pos[parent_pos]}" if parent_pos else str(current_pos[parent_pos])
            bom_structure_dict.append({'pos': pos, 'group_id': group_id})
            hierarchy.append({'pos': pos, 'right': right})

        return bom_structure_dict

    @staticmethod
    def _updateHierarchy(hierarchy: list, left: int) -> list:
        """
        Update the hierarchy by removing elements that end to the right of left.

        Args:
            hierarchy (list): Current hierarchy.
            left (int): Left value of the current node.

        Returns:
            list: Updated hierarchy.
        """
        while hierarchy and hierarchy[-1]['right'] < left:
            hierarchy.pop()
        return hierarchy #Gibt aktualisierte Hierarchie zurück, wobei alle Elemente entfernt wurden, die rechts von left enden.

    @staticmethod
    def _updateCurrentPosition(current_pos: dict, parent_pos: str) -> dict:
        """
        Update the current position dictionary by incrementing 
        the counter for the current parent position.

        Args:
            current_pos (dict): 
                Dictionary with counters for each parent position.
            parent_pos (str): 
                Position of the parent element.

        Returns:
            dict: Updated current position dictionary.
        """
        #current_pos - ein Dictionary, das die Anzahl der Elemente für jede Elternposition enthält, parent_pos - die Position des übergeordneten Elements.
        #Output: Gibt das aktualisierte current_pos-Dictionary zurück, wobei der Zähler für die aktuelle parent_pos-Position erhöht wurde.
        if parent_pos in current_pos:
            current_pos[parent_pos] += 1
        else:
            current_pos[parent_pos] = 1
        return current_pos




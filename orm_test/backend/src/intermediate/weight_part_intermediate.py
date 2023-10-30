from backend.src.manager import PartManager, BillOfMaterialManager, MaterialManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from datetime import datetime, date
from statistics import mean
from backend.src.auxiliary.new_cache import getIdStringFromDict

def checkIfCacheNeedsToExpire(
    dependency: object,
    date: datetime
) -> bool:
    if isinstance(dependency, PartManager):
        weight_changed = (
            not dependency.weight == dependency.__init__(
                dependency.group_id,
                search_date=date,
            ).weight
        )
        material_changed = (
            not dependency.material_manager.material_type == \
                dependency.__init__(
                    dependency.group_id,
                    search_date=date,
                ).material_manager.material_type
        )
        return weight_changed or material_changed
    elif isinstance(dependency, BillOfMaterialManager):
        new_bom = dependency.__init__(
            dependency.group_id,
            search_date=date,
        )
        old_id = getIdStringFromDict(
            dependency.bill_of_material_structure_dict_list
        )
        new_id = getIdStringFromDict(
            new_bom.bill_of_material_structure_dict_list
        )
        return not old_id == new_id

    elif isinstance(dependency, MaterialManager):
        return not dependency.material_type == dependency.__init__(
            dependency.group_id,
            search_date=date,
        ).material_type
    else:
        return True


class WeightIntermediate(GeneralIntermediate):
    relevant_scenario_keys = []
    cacheExpirationCheck = lambda self, dependency, date:(
        checkIfCacheNeedsToExpire(dependency, date)
    )

    def __init__(
        self,
        part_group_id: int,
        search_date: datetime | None = None,
        scenario_dict: dict = {},
    ):
        
        self.part_manager = PartManager(
            group_id=part_group_id,
            search_date=search_date,
        )
        self.bom_manager_list = self.part_manager.bill_of_material_manager_list

        # weight_detail_dict_list is a list of dictionaries, each of which is a bom_manager
        self.weight_detail_dict_list = [
            self.__getWeightDetails(bom_manager)
            for bom_manager in self.bom_manager_list
        ]

        # declare gross weights, mean of each bom_manager
        self.gross_weight = self.__getAverageWeight('gross_weight')
        self.alu_gross_weight = self.__getAverageWeight('alu_gross_weight')
        self.steel_gross_weight = self.__getAverageWeight('steel_gross_weight')
        self.other_gross_weight = self.__getAverageWeight('other_gross_weight')

        # declare net weights, mean of each bom_manager
        self.net_weight = self.__getAverageWeight('net_weight')
        self.alu_net_weight = self.__getAverageWeight('alu_net_weight')
        self.steel_net_weight = self.__getAverageWeight('steel_net_weight')
        self.other_net_weight = self.__getAverageWeight('other_net_weight')

        self.super().__init__(
            search_date,
            scenario_dict,
        )

    @property
    def current_weight(self) -> dict:
        """
        Returns a dictionary containing the current weight values of the object.

        Returns
        -------
        dict
        """
        return {
            'gross_weight': self.gross_weight,
            'alu_gross_weight': self.alu_gross_weight,
            'steel_gross_weight': self.steel_gross_weight,
            'other_gross_weight': self.other_gross_weight,
            'net_weight': self.net_weight,
            'alu_net_weight': self.alu_net_weight,
            'steel_net_weight': self.steel_net_weight,
            'other_net_weight': self.other_net_weight,
        }
    
    def __getAverageWeight(
        self,
        weight_type: str,
        bom_type: str = 'product_development'
    ) -> float:
        """
        Returns the average weight of a specific type of material
        in the object's weight detail list.

        Parameters
        ----------
        weight_type : str
            The type of weight to calculate the average for.
            This should be one of the keys in the weight_detail_dict.
        bom_type : str, optional
            The type of bill of materials to use.
            This should be one of the keys in the weight_detail_dict[bom_type].
            ['product_development', 'industrial_engineering', 'logistic']

        Returns
        -------
        float
            The average weight of the specified type of material
            in the weight detail list.
        """
        weight_list = [
            weight_detail_dict[bom_type][weight_type]
            for weight_detail_dict in self.weight_detail_dict_list
        ]
        return mean(weight_list)
    
    def __getWeightDetails(self, bom_manager: BillOfMaterialManager) -> dict:
        weight_detail_dict = {
            'bom_manager': bom_manager,
            'net_weight': 0,
            'gross_weight': 0,
            'alu_gross_weight': 0,
            'steel_gross_weight': 0,
            'other_gross_weight': 0,
            'net_weight': 0,
            'alu_net_weight': 0,
            'steel_net_weight': 0,
            'other_net_weight': 0,
        }
        weight_dict = {}
        for key in ['product_development', 'industrial_engineering', 'logistic']:
            bom_data_dict = bom_manager.getBillOfMaterialDetails(
                key,
                head_part_group_id=self.part_manager.group_id
            )

            weight_dict = {
                **weight_dict,
                key: {
                    **weight_detail_dict,
                    **self.__getGrossWeight(bom_data_dict),
                    **self.__getNetWeight(bom_data_dict)
                }
            }

        return weight_dict
    
    def __getGrossWeight(self, bom_data_dict: dict) -> dict:
        leaf_part_list = bom_data_dict['leaf_node_list']
        weight_dict = {
            'gross_weight': 0,
            'alu_gross_weight': 0,
            'steel_gross_weight': 0,
            'other_gross_weight': 0,
        }
        connection_dict = {
            'aluminum': 'alu_gross_weight',
            'steel': 'steel_gross_weight',
        }
        for leaf_part in leaf_part_list:
            relative_quantity = leaf_part['relative_quantity']
            weight_dict['gross_weight'] += (
                self.part_manager.weight * relative_quantity
            )
            material_type_name = leaf_part.materiel_manager.material_type.name
            if material_type_name in connection_dict.keys():
                weight_type = connection_dict[
                    material_type_name
                ]
                weight_dict[weight_type] += (
                    self.part_manager.weight * relative_quantity
                )
            else:
                weight_dict['other_gross_weight'] += (
                    self.part_manager.weight * relative_quantity
                )

        return weight_dict

    def __getNetWeight(self, bom_data_dict: dict) -> dict:
        total_net_weight = self.part_manager.weight
        own_material_type = self.part_manager.material_manager.material_type.name
        
        weight_dict = {
            'net_weight': total_net_weight,
            'alu_net_weight': 0,
            'steel_net_weight': 0,
            'other_net_weight': 0,
        }
        connection_dict = {
            'aluminum': 'alu_net_weight',
            'steel': 'steel_net_weight',
        }
        if own_material_type in connection_dict.keys():
            weight_dict[connection_dict[own_material_type]] = total_net_weight
            main_material_type = connection_dict[own_material_type]
        else:
            weight_dict['other_net_weight'] = total_net_weight
            main_material_type = 'other_net_weight'

        direct_child_part_list = bom_data_dict['direct_child_node_list']
        for child_part_data in direct_child_part_list:
            child_part = child_part_data['part']
            relative_quantity = child_part_data['relative_quantity']
            weight = child_part.weight
            material_type_name = child_part.material_manager.material_type.name
            if material_type_name != own_material_type:
                weight_dict[main_material_type] -= weight * relative_quantity
                if material_type_name in connection_dict.keys():
                    weight_dict[connection_dict[material_type_name]] += (
                        weight * relative_quantity
                    )
                else:
                    weight_dict['other_net_weight'] += (
                        weight * relative_quantity
                    )
        
        return weight_dict
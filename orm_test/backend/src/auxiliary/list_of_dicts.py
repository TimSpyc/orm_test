from datetime import datetime


def groupListOfDictsByListOfStrings(
    result_list_dict: list[dict],
    group_by_list: list[str]
) -> list[dict]:
    _checkGroupByFormat(group_by_list, result_list_dict)
    
    level_1_list, level_2_dict = _getGroupLevelDict(group_by_list)
    grouped_data = _buildGroups(result_list_dict, level_1_list)
    return _combineData(grouped_data, level_1_list, level_2_dict)

def _checkGroupByFormat(
    group_by_list: list[str],
    result_list_dict: list[dict]
) -> None:
    if type(group_by_list) is not list:
        raise ValueError('group_by_list must be a list of strings')     
    
    for group in group_by_list:
        if type(group) is not str:
            raise ValueError('group_by_list must be a list of strings')
        group_list = group.split('.')
        if len(group_list) > 2:
            raise Exception("Group by is not supported for more than 2 levels")

        if group_list[0] not in result_list_dict[0].keys():
            raise Exception(f"Group by key {group_list[0]} not found")

def _getGroupLevelDict(group_by_list: list[str]) -> list[str]:
    group_level_dict = {}
    for group in group_by_list:
        group_list = group.split('.')
        if group_list[0] not in group_level_dict:
            group_level_dict[group_list[0]] = []
        if len(group_list) == 2:
            group_level_dict[group_list[0]].append(group_list[1])
    level_1_list = [
        data for data, values in group_level_dict.items()
        if len(values) == 0
    ]
    level_2_dict = {
        data: values for data, values in group_level_dict.items()
        if len(values) != 0
    }
    return level_1_list, level_2_dict

def _buildGroups(data, group_by_list):
    groups = {}
    for item in data:
        key = tuple([item[key] for key in group_by_list])
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

def _combineData(self, data, level_1_list, level_2_dict):
    output_data = []
    for group_data_list in data.values():    
        list_for_combined_data = _buildListForToCombineData(group_data_list)
        combined_data = _combineGroupedData(list_for_combined_data, level_1_list, level_2_dict)
        output_data.append(combined_data)
    return output_data

def _buildListForToCombineData(group_data_list):
    combined_data = {}
    for data in group_data_list:
        for key, value in data.items():
            if key not in combined_data:
                combined_data[key] = []
            combined_data[key].append(value)
    return combined_data

def _combineGroupedData(self, combined_data, level_1_list, level_2_dict):
    group_by_list = level_1_list
    for key, value in combined_data.items():
        if "_id" in key:
            value = [str(x) for x in set(value)]
        if key in group_by_list:
            combined_data[key] = value[0]
        elif all(x is None for x in value):
            combined_data[key] = None
            continue
        elif any(x is None for x in value):
            value = [
                str(x) for x in set(value) if x is not None
            ]
        if all(isinstance(x, int) or isinstance(x, float) for x in value):
            combined_data[key] = sum(value)
        elif all(isinstance(x, str) for x in value):
            combined_data[key] = ", ".join(set(value))
        elif all(isinstance(x, list) for x in value):
            combined_data[key] = [item for sublist in value for item in sublist]
            if key in level_2_dict.keys():
                combined_data[key] = self._combineData(
                    self._buildGroups(combined_data[key], level_2_dict[key]),
                level_2_dict[key], [])
        elif all(isinstance(x, datetime) for x in value):
            combined_data[key] = max(value)
        else:
            raise Exception(f"Cannot combine {key} with values {value}")
    return combined_data
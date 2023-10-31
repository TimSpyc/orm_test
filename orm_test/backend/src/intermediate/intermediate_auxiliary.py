from backend.src.auxiliary.exceptions import NotValidConfigurationError
from collections import defaultdict

def checkValidityOfVolumeDerivativeIntermediateClass(
    self,
    attribute_name,
    possible_values
):
    attribute = getattr(self, attribute_name)
    
    if attribute not in possible_values:
        raise NotValidConfigurationError(
            f"{attribute} is not supported"
        )

def calculateShipment(volume_dict, current_weight_dict):
    '''
    Description:
    ------------
    Calculates the shipment data based on the volume and current weight data.

    Returns:
    --------
    total_shipment : list
        A list of dictionaries containing the shipment data for each date.
    '''
    total_shipment = []
    
    for data in volume_dict:
        date_item = {}
        date_item['date'] = data['date']
        for category, value in current_weight_dict.items():
            date_item[category] = value * data['volume']
        total_shipment.append(date_item)

    return total_shipment

# def GroupByListsOfDictionaries(*lists):
#     '''
#     Description:
#     --------
#     This function takes any number of lists of dictionaries as arguments.
#     It then combines these dictionaries based on the 'date' key,
#     summing the values of any other matching keys.

#     Inputs/Parameters:
#     --------
#     *lists : list of dictionaries
#     Description: Each dictionary in the list should have a 'date' key
#     and any number of additional keys with numeric values.

#     Raises:
#     --------
#     TypeError
#     Description: If the input is not a list of dictionaries or
#     if the dictionaries do not contain the 'date' key.

#     Returns:
#     --------
#     result : list of dictionaries
#     Description: A list of dictionaries, each containing a 'date' key and
#     the summed values of any other matching keys from the input dictionaries.

#     Example:
#     --------
#     >>> AddListOfDictionaries(
#         [
#             {'date': '2022-01-01', 'value': 100, 'name': 'test2', sub_dict: [{'sub_value': 10}]},
#             {'date': '2022-01-02', 'value': 200, 'name': 'test1'}
#         ],
#         [
#             {'date': '2022-01-01', 'value': 300, 'name': 'test'},
#         ]
#     )
#     [{'date': '2022-01-01', 'value': 400}, {'date': '2022-01-02', 'value': 200}]
#     '''
#     result = defaultdict(lambda: defaultdict(int))
#     for list in lists:
#         for dict in list:
#             date = dict.pop('date')
#             for key, value in dict.items():
#                 result[date][key] += value
#     return [{'date': k, **dict(v)} for k, v in result.items()]


# group_by = ["date", "name", "sub_dict.sub_value"]
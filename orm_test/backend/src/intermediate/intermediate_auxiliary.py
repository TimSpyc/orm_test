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

def calculateResultBasedOnVolume(volume_dict, category_value_dict) -> list:
    '''
    Description:
    --------
    This function takes a volume dictionary and a category-value dictionary
    as input. It calculates the product of the volume and the category value 
    for each category and returns a list of dictionaries.

    Inputs/Parameters:
    --------
    volume_dict : list of dictionaries
        A list of dictionaries, each with a 'date' and a 'volume' key.

    category_value_dict : dictionary
        A dictionary containing category names as keys and associated values as values.

    Returns:
    --------
    total_result : list of dictionaries
        A list of dictionaries, each with a 'date' key and
        additional keys for each category, where the value is the product of
        the volume and the category value.
    '''
    total_result = []
    
    for data in volume_dict:
        date_item = {}
        date_item['date'] = data['date']
        for category, value in category_value_dict.items():
            date_item[category] = value * data['volume']
        total_result.append(date_item)

    return total_result

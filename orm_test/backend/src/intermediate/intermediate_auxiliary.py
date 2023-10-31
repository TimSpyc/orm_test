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
        date_item['shipment_data'] = data['volume_date']
        for category, value in current_weight_dict.items():
            date_item[category] = value * data['volume']
        total_shipment.append(date_item)

    return total_shipment

def AddListOfDictionaries(*lists):
    # Combine all the lists
    combined = [item for sublist in lists for item in sublist]

    # Create a defaultdict to store the summed weights
    result = defaultdict(lambda: defaultdict(int))

    # Iterate over the dictionaries in the combined list
    for dict_ in combined:
        # Iterate over the dates and weights in each dictionary
        for date, weights in dict_.items():
            # Iterate over the weight categories and values
            for weight_category, value in weights.items():
                # Add the value to the corresponding entry in the result
                result[date][weight_category] += value

    # Convert the defaultdict back into a regular dict
    result = {date: dict(weights) for date, weights in result.items()}

    # Convert the result into a list of dictionaries
    result = [result]

    return result
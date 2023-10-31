from backend.src.auxiliary.exceptions import NotValidConfigurationError

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

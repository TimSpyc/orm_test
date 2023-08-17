# Responsible Maximilian Kelm
from rest_framework.response import Response
from rest_framework import status
import json
from dateutil.relativedelta import relativedelta

from backend.src.auxiliary.exceptions import NonExistentGroupError, NotUpdatableError, NotValidIdError
import datetime

format_of_valid_14_digit_integer_date = '%Y%m%d%H%M%S'


def addPrefixToDict(
        dict_to_prefix: dict, 
        prefix: str, 
        separator: str ="__"
    ) -> dict:
    """
    The values of the passed dict are stored under the newly composed key. The 
    new key is made up of prefix + separator and the previous key. The separator 
    is optional and is defined by two underscores by default.

    Args:
        dict_to_prefix (dict): 
            Dictionary with values that are to be stored under the newly 
            composed keys
        prefix (str): 
            Text that is placed in front of the newly composed key
        separator (str): 
            Text that separate the prefix and the previous key

    Returns:
        dict: 
            Collection of newly compiled keys and associated values
    """
    return {
        prefix + separator + key: value for key, value in dict_to_prefix.items()
    }

def convertDatetimeObjectTo14DigitInteger(
        datetime_object,
        stringformat=format_of_valid_14_digit_integer_date):

    # TODO das kann dann auch richtig geschrieben werden? ohne string vergleich
    if str(datetime_object) == 'NaT' or datetime_object is None:
        return None
    
    if datetime_object == '-':
        return None

    try:
        return int(datetime_object.strftime(stringformat))

    except Exception as e:
        # print(e, 'given object could not be converted to number')

        # return datetime_object
        return None

def getDate(date=None):
    """
    This function creates a date integer if the kwarg is None. By default
    this argument is None. If it is not None the algorithm checks if the date
    is of type integer and if date is as long as 14 digits. If this is true the
    14 digit integer is returned otherwise a ValueError raises

    Args:
        date (int, optional): int value of a certain date. Defaults to None.
        Input:  Date (e.g. 20200110121500) (default = None)
    Raises:
        ValueError: if the given input isn't of type int or the length isn't 14
        this error raises.

    Returns:
        int: date with a 14 digit number with this format: YYYYMMDDhhmmss
    """

    # TODO #3094 plausibility check of int in getDate() is missing input like 20223540000000 is now interpreted as valid

    if date is None:
        date = convertDatetimeObjectTo14DigitInteger(datetime.datetime.now())

    convert14DigitIntegerIntoDateTimeObject(date)

    return date

def createDateTimeObjectFromString(
    date_string,
    format=format_of_valid_14_digit_integer_date
):

    # check if everything is defined at this position
    # man kann auch andere valide datetime formate wählen
    # write docstring
    # write tsets

    return datetime.datetime.strptime(date_string, format)

def convert14DigitIntegerIntoDateTimeObject(date_integer_to_convert):
    """
    This function is able to convert a given 14 digit integer number to
    a datetimeobject, with the respective properties. The Number is transformed
    to the datetime object if the string format corresponds to the number itself.
    Since the format is defined globally only 14 digit and no other smaller 
    numbers are valid.

    Invalid entries; e.g.:
        - 20223040000000
        - '20223040000000'
        - 2022
        - 202206 
        - ...

    Args:
        date_integer_to_convert (int): standard integer format for date

    Raises:
        ValueError: raises if the given number is not standard format

    Returns:
        datetime object: the datetimeobject of the given integer number
    """

    try:

        datetime_obj = createDateTimeObjectFromString(
            str(date_integer_to_convert),
            format=format_of_valid_14_digit_integer_date
        )
        return datetime_obj

    except Exception:
        raise ValueError(f"""
            Given integer: {date_integer_to_convert} is not a valid date. 
            Please check for typos!""")

def convertSearchDateToDatetimeObject(search_date, add_delta=True):
    """
    ?

    Args:
        search_date (int|None): 
            ?
        add_delta (bool): 
            ?

    Returns:
        datetime|None: 
            ?
    """
    # NOTE There is no auxiliary function to add a time delta to datetime 
    # objects. Because of this the date integer is converted to datetime, added
    # a delta and converted back to integer. After this the function convert the
    # integer back to a datetime object. This is not practical at all!!!
    temp_date = search_date

    if temp_date is not None:
        if add_delta:
            temp_date = timedeltaFromGivenDateInteger(
                temp_date, 1, "seconds"
            )

        return convert14DigitIntegerIntoDateTimeObject(temp_date)

    return None

def timedeltaFromGivenDateInteger(date, delta, increment='days'):
    # function can be enhanced to handle datetimeobjects directly
    # NOTE negative values for delta are also a valid input! but only integeres!

    # this list describes the valid increments
    list_of_valid_increments = [
        'years',
        'months',
        'days',
        'weeks',
        'hours',
        'minutes',
        'seconds',
        'microseconds',
    ]

    try:
        # supposedly given date is an integer!
        date = getDate(date)

    except Exception as e:
        print('Given date is of wrong format. It is not possible to calculate delta: ', e)
        return

    datetime_obj = convert14DigitIntegerIntoDateTimeObject(date)

    # figure out which module is needed to calculate the delta of time:
    if increment not in list_of_valid_increments:
        raise ValueError(f"""
            Given time_increment "{increment}" is not supported. 
            Check documentaion."""
                         )

    if increment == 'years':
        datetime_obj += relativedelta(years=delta)
    elif increment == 'months':
        datetime_obj += relativedelta(months=delta)
    elif increment == 'days':
        datetime_obj += relativedelta(days=delta)
    elif increment == 'weeks':
        datetime_obj += relativedelta(weeks=delta)
    elif increment == 'seconds':
        datetime_obj += relativedelta(seconds=delta)
    elif increment == 'microseconds':
        datetime_obj += relativedelta(microseconds=delta)
    elif increment == 'minutes':
        datetime_obj += relativedelta(minutes=delta)
    elif increment == 'hours':
        datetime_obj += relativedelta(hours=delta)
    elif increment == 'weeks':
        datetime_obj += relativedelta(weeks=delta)

    date_delta_integer = convertDatetimeObjectTo14DigitInteger(datetime_obj)

    return date_delta_integer

def reduceManagerInfo(manager_data_dict, info_key_list):
    """
    ?

    Args:
        manager_data_dict (dict|None): 
            ?
        info_key_list (dict|None): 
            ?

    Returns:
        dict: 
            ?
    """
    reduced_info_dict = {}

    if info_key_list is not None and manager_data_dict is not None:
        for key in info_key_list:
            if key in manager_data_dict.keys():
                reduced_info_dict[key] = manager_data_dict[key]

    return reduced_info_dict

def reduceDictWithKeyList(
    dict_to_reduce, 
    wanted_key_list
):
    """
    ?

    Args:
        dict_to_reduce (dict): 
            ?
        wanted_key_list (list|None): 
            ?

    Returns:
        dict: 
            ?
    """
    if wanted_key_list is None:
        return dict_to_reduce
    
    reduced_dict = {}

    for key in wanted_key_list:
        if key in dict_to_reduce.keys():
            reduced_dict[key] = dict_to_reduce[key]

    return reduced_dict

def readKeyFromQueryParams(query_params: dict, wanted_key: str):
    """
    ?

    Args:
        query_params (dict): 
            ?
        wanted_key (str): 
            ?

    Returns:
        any: 
            ?
    """
    if wanted_key in query_params.keys():
        return query_params[wanted_key]

    return None

def readSearchDateFromQueryParamsAndConvertToDatetimeObject(query_params: dict):
    search_date = readKeyFromQueryParams(query_params, "search_date")
    
    if search_date is not None:
        return convertSearchDateToDatetimeObject(search_date)

    return None

def readFilterFromQueryParamsAndConvertToDict(query_params: dict):
    filter_str = readKeyFromQueryParams(query_params, "filter")
    
    if filter_str is not None:
        return json.loads(filter_str)

    return {}

def _errorIfDateIsNotSpecified(manager_data_dict):
    if "date" not in manager_data_dict.keys():
        raise ValueError("Date must be specified!")

def readDataFromRequestObject(request):
    """
    ?

    Args:
        request (Request): 
            ?

    Returns:
        dict: 
            ?
    """
    return request.data

def readCreatorIdFromRequestObject(request):
    """
    ?

    Args:
        request (Request): 
            ?

    Returns:
        int: 
            ?
    """
    return request.user.id

def responseIfMethodNotAvailable():
    """
    ?

    Returns:
        Response: 
            ?
    """
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def adjustStatusWithResponse(response):
    """
    ?

    Args:
        response (any): 
            ?

    Returns:
        Response: 
            ?
    """
    temp_status = status.HTTP_200_OK

    if type(response) in [dict, list] and len(response) == 0:
        temp_status = status.HTTP_204_NO_CONTENT

    return Response(data=response, status=temp_status)

def catchErrorsAndAdjustResponse(createRequestResponse):
    """
    ?

    Args:
        createRequestResponse (func): 
            ?

    Returns:
        Response: 
            ?
    """
    try:
        return adjustStatusWithResponse(createRequestResponse())
    except ValueError as e:
        print("ValueError: ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except NonExistentGroupError as e:
        print("NonExistentGroupError: ", e)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except NotUpdatableError as e:
        print("NotUpdatableError: ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except NotValidIdError as e:
        print("NotValidIdError: ", e)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("Exception: ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# TODO create function to check query params for unwanted information!
def errorIfQueryParamsContainUnwantedInformation(query_params, allowed_keys=[]):
    """
    ?

    Args:
        query_params (dict): 
            ?
        allowed_keys (list): 
            ?

    Raises:
        ValueError: ?.
    """
    for key in query_params.keys():
        if key not in allowed_keys:
            raise ValueError("Unwanted key: " + key)
        
def convertListToTupleInFilterDict(filter_dict: dict) -> dict:
    """
    ?

    Args:
        filter_dict (dict): 
            ?

    Returns:
        dict: 
            ?
    """
    temp_converted_filter_dict = {}

    for key, value in filter_dict.items():
        if type(value) == list:
            temp_converted_filter_dict[key] = tuple(value)
        else:
            temp_converted_filter_dict[key] = value

    return temp_converted_filter_dict

def readAndConvertFilterDict(query_params: dict) -> dict:
    """
    ?

    Args:
        query_params (dict): 
            ?

    Returns:
        dict: 
            ?
    """
    return convertListToTupleInFilterDict(
        readFilterFromQueryParamsAndConvertToDict(query_params)
    )

################################################################################
##### Handle manager method functions ##########################################
################################################################################
def isValidInt(int_value):
    # TODO #4836 docstring is missing; please explain your function
    try:
        int(int_value)
        return True
    except ValueError:
        return False


def isValidFloat(float_value):
    # TODO #4836 docstring is missing; please explain your function
    try:
        float(float_value)
        return True
    except ValueError:
        return False

def isValidList(list_value):
    # TODO #4836 docstring is missing; please explain your function
    try:
        if type(list_value) is list:
            return True
        else:
            is_list = json.loads(list_value)       
        if type(is_list) is not list:
            return False
        return True
    except:
        return False


def queryParamsIntoDict(request):
    '''
    The information from the url is returned in its basic form as dict.

    Parameters
    ----------
    request : rest_framework.request.Request
        Contains the query dict with the information passed via the url.

    Returns
    -------
    query_params_dict : dict
        Contains the information passed via the url in its basic form.
    '''
    query_params_dict = dict(request.query_params)

    if len(query_params_dict) > 0:
        
        temp_query_params_dict = dict()
        
        # TODO Possibly recognize and convert additional data types 
        
        for key, value in query_params_dict.items():
            
            if isValidInt(value[0]):
                temp_query_params_dict[key] = int(value[0])
            elif isValidFloat(value[0]):
                temp_query_params_dict[key] = float(value[0])
            elif isValidList(value[0]):
                temp_query_params_dict[key] = json.loads(value[0])
            else:
                temp_query_params_dict[key] = value[0]

        return temp_query_params_dict
    
    return query_params_dict

def getReducedAndFilteredManagerData(manager, createManagerInfoDict, request):
    def createRequestResponse():
        query_params = queryParamsIntoDict(request)
        wanted_key_list = readKeyFromQueryParams(query_params, "wanted_keys")
        filter_dict = readAndConvertFilterDict(query_params)
        search_date = readSearchDateFromQueryParamsAndConvertToDatetimeObject(
            query_params
        )

        return [
            reduceDictWithKeyList(
                createManagerInfoDict(manager_obj), wanted_key_list
            ) for manager_obj in manager.filter(
                search_date=search_date, **filter_dict
            )
        ]
    
    return catchErrorsAndAdjustResponse(createRequestResponse)

def getReducedManagerData(
    manager_group_id, 
    manager, 
    createManagerInfoDict, 
    request
):
    def createRequestResponse():
        query_params = queryParamsIntoDict(request)
        wanted_key_list = readKeyFromQueryParams(query_params, "wanted_keys")
        search_date = readSearchDateFromQueryParamsAndConvertToDatetimeObject(
            query_params
        )

        return reduceDictWithKeyList(
            createManagerInfoDict(
                manager(manager_group_id, search_date=search_date)
            ), 
            wanted_key_list
        )

    return catchErrorsAndAdjustResponse(createRequestResponse)

def createManager(manager, request):
    def createRequestResponse():
        query_params = queryParamsIntoDict(request)
        errorIfQueryParamsContainUnwantedInformation(query_params)
        data_to_create = readDataFromRequestObject(request)
        creator_id = readCreatorIdFromRequestObject(request)

        manager_obj = manager.create(creator_id, **data_to_create)        

        return manager_obj.group_id

    return catchErrorsAndAdjustResponse(createRequestResponse)

def updateManager(manager_group_id, manager, request):
    def createRequestResponse():
        data_to_update = readDataFromRequestObject(request)
        creator_id = readCreatorIdFromRequestObject(request)
        query_params = queryParamsIntoDict(request)
        allowed_keys = ["search_date"]
        errorIfQueryParamsContainUnwantedInformation(query_params, allowed_keys)
        search_date = readSearchDateFromQueryParamsAndConvertToDatetimeObject(
            query_params
        )

        manager_obj = manager(manager_group_id, search_date=search_date)
        manager_obj.update(
            creator_id, **data_to_update
        )

        return manager_obj.group_id

    return catchErrorsAndAdjustResponse(createRequestResponse)

def deactivateManager(manager_group_id, manager, request):
    def createRequestResponse():
        creator_id = readCreatorIdFromRequestObject(request)
        query_params = queryParamsIntoDict(request)
        allowed_keys = ["search_date"]
        errorIfQueryParamsContainUnwantedInformation(query_params, allowed_keys)
        search_date = readSearchDateFromQueryParamsAndConvertToDatetimeObject(
            query_params
        )

        manager_obj = manager(manager_group_id, search_date=search_date)
        manager_obj.deactivate(creator_id)

        return manager_obj.group_id

    return catchErrorsAndAdjustResponse(createRequestResponse)


################################################################################
##### Handle manager request methods ###########################################
################################################################################
def handleManagerRequestMethods_detail(
    request, 
    manager, 
    manager_group_id, 
    serializeManagerFunction
):
    if request.method == 'GET':
        return getReducedManagerData(
            manager_group_id,
            manager,
            serializeManagerFunction,
            request
        )

    elif request.method == 'PUT':
        return updateManager(
            manager_group_id,
            manager,
            request
        )

    elif request.method == 'DELETE':
        return deactivateManager(
            manager_group_id,
            manager,
            request
        )

    else:
        return responseIfMethodNotAvailable()

def handleManagerRequestMethods_list(
    request, 
    manager, 
    serializeManagerFunction
):
    if request.method == 'GET':
        return getReducedAndFilteredManagerData(
            manager,
            serializeManagerFunction,
            request
        )

    elif request.method == 'POST':
        return createManager(
            manager,
            request
        )

    else:
        return responseIfMethodNotAvailable()

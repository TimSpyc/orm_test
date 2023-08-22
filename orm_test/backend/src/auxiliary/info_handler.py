# Responsible Maximilian Kelm
from rest_framework.response import Response
from rest_framework import status
import json
import logging

from backend.src.auxiliary.exceptions import NonExistentGroupError, NotUpdatableError, NotValidIdError
import backend.src.auxiliary.temp_auxiliary_master as aux
    
#### potential aux functions ###################################################
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
            temp_date = aux.timedeltaFromGivenDateInteger(
                temp_date, 1, "seconds"
            )

        return aux.convert14DigitIntegerIntoDateTimeObject(temp_date)

    return None

def reduceDictWithKeyList(dict_to_reduce: dict, wanted_key_list: list) -> dict:
    """
    Reduces a dictionary to a subset of keys specified in a list.

    This function takes a dictionary and a list of keys as input and returns a 
    new dictionary that contains only the key-value pairs whose keys are in the 
    list. If the list or dict is None, the function returns the original 
    dictionary.

    Args:
        dict_to_reduce (dict): The dictionary to reduce.
        wanted_key_list (list or None): The list of keys to keep in the reduced 
                                        dictionary.

    Returns:
        dict: A new dictionary containing only the key-value pairs whose keys 
                are in the list.
    """
    if wanted_key_list is None or dict_to_reduce is None:
        return dict_to_reduce
    
    return {
        key: dict_to_reduce[key]\
                for key in wanted_key_list\
                if key in dict_to_reduce
    }

def convertListToTupleInFilterDict(filter_dict: dict) -> dict:
    """
    Converts any lists in a filter dictionary to tuples.

    This function takes a dictionary representing filter criteria as input and 
    converts any lists in the dictionary to tuples, since lists are not hashable 
    and cannot be used as keys in a dictionary. The resulting dictionary is 
    returned.

    Args:
        filter_dict (dict): A dictionary representing filter criteria.

    Returns:
        dict: A dictionary representing the filter criteria, with any lists 
                converted to tuples.
    """
    return {
        key: tuple(value) if isinstance(value, list) else value\
                for key, value in filter_dict.items()
    }

#### read info from url ########################################################
def readKeyFromQueryParams(query_params: dict, wanted_key: str):
    """
    Extracts a value from the query parameters based on a given key.

    This function takes a dictionary of query parameters as input and a string 
    representing the key to extract. If the key is present in the dictionary, 
    the function returns the corresponding value. Otherwise, None is returned.

    Args:
        query_params (dict): A dictionary of query parameters.
        wanted_key (str): The key to extract from the query parameters.

    Returns:
        any: The value associated with the given key, or None if the key is not 
        present in the query parameters.
    """
    return query_params[wanted_key]\
            if wanted_key in query_params.keys() else None

def readSearchDateFromQueryParamsAndConvertToDatetimeObject(query_params: dict):
    """
    Extracts a search date string from the query parameters and converts it to a 
    datetime object.

    This function takes a dictionary of query parameters as input and extracts 
    the value associated with the "search_date" key. If the value is not None, 
    the function uses the `convertSearchDateToDatetimeObject` helper function to 
    convert the value to a datetime object. Otherwise, None is returned.

    Args:
        query_params (dict): A dictionary of query parameters.

    Returns:
        datetime.datetime or None: A datetime object representing the search 
        date, or None if the search date is not present in the query parameters 
        or is invalid.
    """
    search_date = readKeyFromQueryParams(query_params, "search_date")
    
    return convertSearchDateToDatetimeObject(
        search_date
    ) if search_date is not None else None

def readFilterFromQueryParamsAndConvertToDict(query_params: dict):
    """
    Extracts a filter string from the query parameters and converts it to a 
    dictionary.

    This function takes a dictionary of query parameters as input and extracts 
    the value associated with the "filter" key. If the value is not None, the 
    function uses the `json.loads` method to convert the value to a dictionary. 
    Otherwise, an empty dictionary is returned.

    Args:
        query_params (dict): A dictionary of query parameters.

    Returns:
        dict: A dictionary representing the filter criteria.
    """
    filter_str = readKeyFromQueryParams(query_params, "filter")
    
    return json.loads(filter_str) if filter_str is not None else {}

#### read info from request object #############################################
def readDataFromRequestObject(request):
    """
    Extracts the data payload from a Django `Request` object.

    This function takes a Django `Request` object as input and returns the data 
    payload associated with the request. The data payload typically contains 
    information submitted by the client in the request body, such as form data 
    or JSON-encoded data.

    Args:
        request (Request): The Django `Request` object representing the incoming 
                            HTTP request.

    Returns:
        dict: A dictionary containing the data payload associated with the 
                request.
    """
    return request.data

def readCreatorIdFromRequestObject(request):
    """
    Extracts the ID of the user who made the request.

    This function takes a Django `Request` object as input and returns the ID of 
    the user who made the request. The ID is typically used to associate the 
    request with a particular user in the database.

    Args:
        request (Request): The Django `Request` object representing the incoming 
                            HTTP request.

    Returns:
        int: The ID of the user who made the request.
    """
    return request.user.id

#### handle errors and response status #########################################
def responseIfMethodNotAvailable():
    """
    Returns a HTTP 405 Method Not Allowed response.

    This function is typically used as a fallback response when a client tries 
    to use an HTTP method that is not supported by the server for a particular 
    resource.

    Returns:
        Response: A Response object with a status code of 405 
                    => (Method Not Allowed).
    """
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def adjustStatusWithResponse(response):
    """
    Adjusts the HTTP status code based on the response data.

    This function takes a response object as input and adjusts the HTTP status 
    code based on the type and content of the response data. If the response 
    data is a dictionary or list with zero elements, the function sets the 
    status code to 204 (No Content). Otherwise, the status code is set to 200 
    (OK).

    Args:
        response (any): The response object to adjust the status code for.

    Returns:
        Response: A Response object with the adjusted status code.
    """
    temp_status = status.HTTP_200_OK

    if type(response) in [dict, list] and len(response) == 0:
        temp_status = status.HTTP_204_NO_CONTENT

    return Response(data=response, status=temp_status)

# TODO Put the status code in the exception class!
def selectStatusWithErrorType(error_type):
    """
    Maps an exception type to an HTTP status code.

    This function takes an exception type as input and returns the corresponding 
    HTTP status code based on the type of the exception. If the exception type 
    is not in the mapping, the function returns a default status code of 400 
    (Bad Request).

    Args:
        error_type (type): The type of the exception to map to an HTTP status 
                            code.

    Returns:
        int: The HTTP status code corresponding to the exception type.
    """
    return {
        ValueError: status.HTTP_400_BAD_REQUEST,
        NonExistentGroupError: status.HTTP_404_NOT_FOUND,
        NotUpdatableError: status.HTTP_400_BAD_REQUEST,
        NotValidIdError: status.HTTP_404_NOT_FOUND
    }.get(type(error_type), status.HTTP_400_BAD_REQUEST)
    
def catchErrorsAndAdjustResponse(createRequestResponse):
    """
    Handles exceptions that may be raised by the createRequestResponse function 
    and adjusts the HTTP status code of the response accordingly.

    This function takes a function as input that returns a response object. It 
    calls the function and catches any exceptions that may be raised. If an 
    exception is caught, the function uses the `selectStatusWithErrorType` 
    helper function to determine the appropriate HTTP status code to use in the 
    response. If no exception is caught, the function uses the 
    `adjustStatusWithResponse` helper function to adjust the HTTP status code 
    based on the response data.

    Args:
        createRequestResponse (func): A function that returns a response object.

    Returns:
        Response: A response object with the adjusted HTTP status code.
    """
    try:
        return adjustStatusWithResponse(createRequestResponse())
    except Exception as e:
        logging.exception(e)
        return Response(status=selectStatusWithErrorType(e))
    

    
#### handle query params #######################################################
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

def readAndConvertFilterDict(query_params: dict) -> dict:
    """
    Reads and converts a filter dictionary from the query parameters.

    This function takes a dictionary of query parameters as input and extracts 
    the filter dictionary from it. It then converts any lists in the filter 
    dictionary to tuples, since lists are not hashable and cannot be used as 
    keys in a dictionary. The resulting dictionary is returned.

    Args:
        query_params (dict): A dictionary of query parameters.

    Returns:
        dict: A dictionary representing the filter criteria, with any lists 
                converted to tuples.
    """
    return convertListToTupleInFilterDict(
        readFilterFromQueryParamsAndConvertToDict(query_params)
    )

##### Handle manager functions #################################################
def getReducedAndFilteredManagerData(manager, createManagerInfoDict, request):
    """
    Returns a reduced and filtered list of manager data based on the HTTP 
    request.

    This function takes a manager object, a function to create a dictionary of 
    manager data, and an HTTP request as input and returns a reduced and 
    filtered list of manager data based on the HTTP request. The function 
    extracts the wanted keys, filter dictionary, and search date from the HTTP 
    request and uses them to create the reduced and filtered list. If any errors 
    occur during the creation process, the function catches them and adjusts the 
    response accordingly.

    Args:
        manager (Manager): The manager object to use for getting data.
        createManagerInfoDict (function): The function to use for creating a 
                                            dictionary of manager data.
        request (HttpRequest): The HTTP request containing the wanted keys, 
                                filter dictionary, and search date.

    Returns:
        HttpResponse: A reduced and filtered list of manager data, or an error 
                        response if an error occurs during the creation process.
    """
    def createRequestResponse():
        query_params = aux.queryParamsIntoDict(request)
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
    """
    Returns a reduced dictionary of manager data based on the HTTP request.

    This function takes a manager group ID, a manager object, a function to 
    create a dictionary of manager data, and an HTTP request as input and 
    returns a reduced dictionary of manager data based on the HTTP request. The 
    function extracts the wanted keys and search date from the HTTP request and 
    uses them to create the reduced dictionary. If any errors occur during the 
    creation process, the function catches them and adjusts the response 
    accordingly.

    Args:
        manager_group_id (int): The ID of the manager group to get data from.
        manager (Manager): The manager object to use for getting data.
        createManagerInfoDict (function): The function to use for creating a 
                                            dictionary of manager data.
        request (HttpRequest): The HTTP request containing the wanted keys and 
                                search date.

    Returns:
        HttpResponse: A reduced dictionary of manager data, or an error response 
                        if an error occurs during the creation process.
    """
    def createRequestResponse():
        query_params = aux.queryParamsIntoDict(request)
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
    """
    Creates a new manager and returns the manager group ID.

    This function takes a manager object and an HTTP request as input and 
    creates a new manager using the data provided in the request. It then 
    returns the manager group ID. The function also extracts the creator ID and 
    data to create from the HTTP request and uses them to create the manager 
    object. If any errors occur during the creation process, the function 
    catches them and adjusts the response accordingly.

    Args:
        manager (Manager): The manager object to use for creation.
        request (HttpRequest): The HTTP request containing the creator ID and 
                                data to create.

    Returns:
        HttpResponse: The manager group ID, or an error response if an error 
                        occurs during the creation process.
    """
    def createRequestResponse():
        query_params = aux.queryParamsIntoDict(request)
        errorIfQueryParamsContainUnwantedInformation(query_params)
        data_to_create = readDataFromRequestObject(request)
        creator_id = readCreatorIdFromRequestObject(request)

        manager_obj = manager.create(creator_id, **data_to_create)        

        return manager_obj.group_id

    return catchErrorsAndAdjustResponse(createRequestResponse)

def updateManager(manager_group_id, manager, request):
    """
    Updates a manager and returns the manager group ID.

    This function takes a manager group ID, a manager object, and an HTTP 
    request as input and updates the manager associated with the group ID. It 
    then returns the manager group ID. The function also extracts the creator 
    ID, search date, and data to update from the HTTP request and uses them to 
    create and update the manager object. If any errors occur during the update 
    process, the function catches them and adjusts the response accordingly.

    Args:
        manager_group_id (int): The ID of the manager group to update.
        manager (Manager): The manager object to use for updating.
        request (HttpRequest): The HTTP request containing the creator ID, 
                                search date, and data to update.

    Returns:
        HttpResponse: The manager group ID, or an error response if an error 
                        occurs during the update process.
    """
    def createRequestResponse():
        data_to_update = readDataFromRequestObject(request)
        creator_id = readCreatorIdFromRequestObject(request)
        query_params = aux.queryParamsIntoDict(request)
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
    """
    Deactivates a manager and returns the manager group ID.

    This function takes a manager group ID, a manager object, and an HTTP 
    request as input and deactivates the manager associated with the group ID. 
    It then returns the manager group ID. The function also extracts the creator 
    ID and search date from the HTTP request and uses them to create the manager 
    object. If any errors occur during the deactivation process, the function 
    catches them and adjusts the response accordingly.

    Args:
        manager_group_id (int): The ID of the manager group to deactivate.
        manager (Manager): The manager object to use for deactivation.
        request (HttpRequest): The HTTP request containing the creator ID and 
                                search date.

    Returns:
        HttpResponse: The manager group ID, or an error response if an error 
                        occurs during the deactivation process.
    """
    def createRequestResponse():
        creator_id = readCreatorIdFromRequestObject(request)
        query_params = aux.queryParamsIntoDict(request)
        allowed_keys = ["search_date"]
        errorIfQueryParamsContainUnwantedInformation(query_params, allowed_keys)
        search_date = readSearchDateFromQueryParamsAndConvertToDatetimeObject(
            query_params
        )

        manager_obj = manager(manager_group_id, search_date=search_date)
        manager_obj.deactivate(creator_id)

        return manager_obj.group_id

    return catchErrorsAndAdjustResponse(createRequestResponse)

##### Handle manager request methods ###########################################
def checkRequestIncludesWantedMethod(request, wanted_method):
    """
    Checks if an HTTP request includes a specific method.

    This function takes an HTTP request and a method as input and returns True 
    if the request includes the method, and False otherwise.

    Args:
        request (HttpRequest): The HTTP request to check.
        wanted_method (str): The HTTP method to check for.

    Returns:
        bool: True if the request includes the method, False otherwise.
    """
    return request.method == wanted_method

def handleManagerRequestMethods_detail(
    request, 
    manager, 
    manager_group_id, 
    serializeManagerFunction
):
    """
    Handles a manager request based on the HTTP method and returns detailed 
    information.

    This function takes an HTTP request, a manager object, a manager group ID, 
    and a serialization function as input and returns detailed information about 
    the manager based on the HTTP method. If the method is not available, the 
    function returns a response indicating that the method is not available.

    Args:
        request (HttpRequest): The HTTP request to handle.
        manager (Manager): The manager object to handle.
        manager_group_id (int): The ID of the manager group to which the manager 
                                belongs.
        serializeManagerFunction (function): The function to use for serializing 
                                                the manager data.

    Returns:
        HttpResponse: The detailed information about the manager, or a response 
                        indicating that the method is not available.
    """
    if checkRequestIncludesWantedMethod(request, 'GET'):
        return getReducedManagerData(
            manager_group_id,
            manager,
            serializeManagerFunction,
            request
        )

    elif checkRequestIncludesWantedMethod(request, 'PUT'):
        return updateManager(
            manager_group_id,
            manager,
            request
        )

    elif checkRequestIncludesWantedMethod(request, 'DELETE'):
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
    """
    Handles a manager list request based on the HTTP method.

    This function takes an HTTP request, a manager object, and a serialization 
    function as input and returns a list of managers based on the HTTP method. 
    If the method is not available, the function returns a response indicating 
    that the method is not available.

    Args:
        request (HttpRequest): The HTTP request to handle.
        manager (Manager): The manager object to handle.
        serializeManagerFunction (function): The function to use for serializing 
                                                the manager data.

    Returns:
        HttpResponse: A list of managers, or a response indicating that the 
                        method is not available.
    """
    if checkRequestIncludesWantedMethod(request, 'GET'):
        return getReducedAndFilteredManagerData(
            manager,
            serializeManagerFunction,
            request
        )

    elif checkRequestIncludesWantedMethod(request, 'POST'):
        return createManager(
            manager,
            request
        )

    else:
        return responseIfMethodNotAvailable()

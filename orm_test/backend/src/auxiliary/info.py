import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.src.auxiliary.manager import GeneralManager
from backend.src.auxiliary.intermediate import GeneralIntermediate
from django.urls import path
from django.http.request import HttpRequest
from backend.src.auxiliary.exceptions import *
import json



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

def catchErrorsAndAdjustResponse(createRequestResponse):
    """
    Wraps a function that creates a request response and catches any errors.

    This function takes a function that creates a request response as input and 
    returns a new function that wraps the original function and catches any 
    errors that occur during its execution. If an error occurs, the function 
    logs the error and returns an error response with an appropriate status 
    code. Otherwise, it returns the response created by the original function.

    Args:
        createRequestResponse (function): A function that creates a request 
                                            response.

    Returns:
        function: A new function that wraps the original function and catches 
                    any errors that occur during its execution.
    """
    def tryExceptWrapper(*args, **kwargs):
        try:
            return adjustStatusWithResponse(
                createRequestResponse(*args, **kwargs)
            )
        except Exception as e:
            logging.exception(e)
            return Response(status=selectStatusWithErrorType(e))
    
    return tryExceptWrapper

def addPrefix(prefix: str, dictionary: dict) -> dict:
    """
    Adds a prefix to all keys in a dictionary.

    This function takes a prefix and a dictionary as input and returns a new 
    dictionary with the same values as the original dictionary, but with the 
    prefix added to all keys.

    Args:
        prefix (str): The prefix to add to all keys.
        dictionary (dict): The dictionary to add the prefix to.

    Returns:
        dict: A new dictionary with the same values as the original dictionary, 
                but with the prefix added to all keys.
    """
    return {
        f'{prefix}_{key}': value
        for key, value in dictionary.items()
    }

class GeneralInfo:
    WITHOUT_IDENTIFIER_OPERATIONS = {'GET_list', 'POST'}
    WITH_IDENTIFIER_OPERATIONS = {'GET_detail', 'PUT', 'DELETE'}
    base_url: str
    allowed_method_list: list # ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list: list
    detail_key_dict: dict = {'group_id': 'int'}

    manager: GeneralManager # Optional
    datasetPermissionFunction = lambda cls, data_set_dict: True
    serializerFunction = lambda cls, data_object : dict(data_object)

    def __new__(
        cls,
        use_cache: bool = False,
        **kwargs: dict
    ) -> 'GeneralInfo':
        if use_cache:
            cached_instance = cls.__handleCache(cls, **kwargs)
            if cached_instance:
                return cached_instance
        instance =  super().__new__(cls)
        instance.__init__(**kwargs)
        return instance

    def getDetail(
        self,
        request: HttpRequest,
        **identifier: dict
    ) -> GeneralManager:
        request_info_dict = self.__getRequestInfos(request)
        search_date = request_info_dict['query_params'].get('search_date', None)
        return self.manager(
            search_date=search_date,
            **identifier,
        )

    def put(
        self,
        request: HttpRequest,
        **identifier: dict
    ) -> None:
        self.__checkConfiguration()
        request_info_dict = self.__getRequestInfos(request)

        manager_obj = self.manager(
            identifier['group_id'],
            request_info_dict['request_data']['creation_date']
        )
        
        manager_obj.update(
                creator_id = request_info_dict["request_user_id"],
                **request_info_dict['request_data']
            )

    def delete(
        self,
        request: HttpRequest,
        **identifier: dict
    ) -> None:
        self.__checkConfiguration()
        request_info_dict = self.__getRequestInfos(request)

        manager_obj = self.manager(
            identifier['group_id'],
            request_info_dict['request_data']['creation_date']
        )
        
        manager_obj.deactivate(
                creator_id = request_info_dict["request_user_id"],
            )

    def getList(
        self,
        request: HttpRequest
    ) -> list[object]:
        request_info_dict = self.__getRequestInfos(request)
        search_date = request_info_dict['query_params'].get('search_date', None)
        filter_dict = request_info_dict['query_params'].get('filter', {})

        return self.manager.filter(
            search_date=search_date,
            **filter_dict,
        )

    def post(
        self,
        request: HttpRequest
    ) -> int:
        self.__checkConfiguration()
        request_info_dict = self.__getRequestInfos(request)

        manager_obj = self.manager.create(
            creator_id = request_info_dict["request_user_id"],
            **request_info_dict['request_data']
        )

        return manager_obj.group_id

    @classmethod
    def __handleCache(cls, **kwargs: dict) -> 'GeneralInfo':
        #TODO: implement
        instance =  super().__new__(cls)
        instance.__init__(**kwargs)
        return instance

    def __checkConfiguration(self) -> None:
        has_manager = hasattr(self, 'manager')
        is_manager = isinstance(self.manager, GeneralManager)

        if not has_manager or not is_manager:
            raise Exception('manager not found')
    
    def __serializeData(
        self,
        data_object: GeneralManager | GeneralIntermediate | object
    ) -> dict:
        return self.serializerFunction(data_object)

    def _handleGetList(self, request: HttpRequest) -> list[dict]:
        object_list = self.getList(request)
        result_list_dict = map(
            lambda manager_obj: self.__serializeData(manager_obj),
            object_list
        )
        result= self.__reduceGetResultList(result_list_dict, request)
        return result

    def _handleGetDetail(self, request: HttpRequest, **identifier) -> dict:
        manager_obj = self.getDetail(request, **identifier)
        result_dict = self.__serializeData(manager_obj)
        return self.__reduceGetResult(result_dict, request)

    def __reduceGetResult(
        self,
        result_dict: dict,
        request: HttpRequest
    ) -> dict:
        request_info_dict = self.__getRequestInfos(request)
        attributes = request_info_dict['query_params'].get('attributes', None)
        if self.__couldBeSend(result_dict):
            return self.__reduceDictWithKeyList(result_dict, attributes)

    def __reduceGetResultList(
        self,
        result_list: list[dict],
        request: HttpRequest
    ) -> list[dict]:
        request_info_dict = self.__getRequestInfos(request)
        attributes = request_info_dict['query_params'].get('attributes', None)

        filtered_and_reduced_list = list(map(
            lambda dict_keys: self.__reduceDictWithKeyList(
                dict_keys,
                attributes
            ), filter(lambda item: self.__couldBeSend(item), result_list)
        ))
        return filtered_and_reduced_list

    def __couldBeSend(self, result_dict: dict) -> bool:
        return self.datasetPermissionFunction(result_dict)

    @classmethod
    def __getAllowedMethodsList(cls, method_type: str) -> list:
        allowed_model_operations = set(cls.allowed_method_list)
        # if method_type not in allowed_model_operations:
        if method_type == 'detail':
            control_list = cls.WITH_IDENTIFIER_OPERATIONS
        elif method_type == 'list':
            control_list = cls.WITHOUT_IDENTIFIER_OPERATIONS
        else:
            raise ValueError('method_type must be "detail" or "list"')

        return [
            allowed_model_operation.split('_')[0]
            for allowed_model_operation in allowed_model_operations
            if allowed_model_operation in control_list
        ]

    @classmethod
    def _getUrl(cls) -> list:
        allowed_detail_methods = cls.__getAllowedMethodsList('detail')
        allowed_list_methods = cls.__getAllowedMethodsList('list')

        @api_view(allowed_list_methods)
        @catchErrorsAndAdjustResponse
        def listRequest(request):
            return cls.__handleManagerRequestMethods_list(request)
        
        @api_view(allowed_detail_methods)
        def detailRequest(request, **identifier):
            return cls.__handleManagerRequestMethods_detail(request, **identifier)
        cls.__checkGeneralInfoIsProperlyConfigured()

        allowed_model_operations = set(cls.allowed_method_list)

        url_list = []

        if cls.WITHOUT_IDENTIFIER_OPERATIONS & allowed_model_operations:
            url_list.append(path(
                f'{cls.base_url}/',
                listRequest
            ))
        if cls.WITH_IDENTIFIER_OPERATIONS & allowed_model_operations:
            identifier_string = '/'.join([
                f'<{key_type}:{key}>'
                for key, key_type in cls.detail_key_dict.items()
            ])

            url_list.append(path(
                f'{cls.base_url}/{identifier_string}',
                detailRequest
            ))

        return url_list

    @classmethod
    def __handleManagerRequestMethods_list(
        cls,
        request: HttpRequest
    ) -> list | int:
        cls.__checkIfUserIsAuthorized(request)
        instance = cls()

        if cls.__checkRequestIncludesWantedMethod(request, 'GET'):
            return instance._handleGetList(request)

        elif cls.__checkRequestIncludesWantedMethod(request, 'POST'):
            return instance.post(request)

        else:
            return cls.__responseIfMethodNotAvailable()

    @classmethod
    def __handleManagerRequestMethods_detail(cls, request, **identifier):
        cls.__checkIfUserIsAuthorized(request)
        instance = cls(**identifier)

        if cls.__checkRequestIncludesWantedMethod(request, 'GET'):
            return instance._handleGetDetail(request, **identifier)

        elif cls.__checkRequestIncludesWantedMethod(request, 'PUT'):
            instance.put(request, **identifier)
            return cls.__responseIfAlright()

        elif cls.__checkRequestIncludesWantedMethod(request, 'DELETE'):
            instance.delete(request, **identifier)
            return cls.__responseIfAlright()
        
        else:
            return cls.__responseIfMethodNotAvailable()

    @staticmethod
    def __checkIfUserIsAuthorized(request):
        #TODO: implement user forwarding if not logged in
        if (
            not request.user.is_authenticated or
            not GeneralInfo.__hasRequiredPermissions(request)
        ):
            # raise Exception('User not authorized')
            pass

    @staticmethod
    def __hasRequiredPermissions(request):
        request
        #TODO: implement
        return True

    @classmethod
    def __checkRequestIncludesWantedMethod(
        cls,
        request: HttpRequest,
        wanted_method: str,
        # method_type: str|None = None
    ) -> bool:
        """
        Checks if an HTTP request includes a specific method.

        This function takes an HTTP request and a method as input and returns
        True if the request includes the method, and False otherwise.

        Args:
            request (HttpRequest): The HTTP request to check.
            wanted_method (str): The HTTP method to check for.

        Returns:
            bool: True if the request includes the method, False otherwise.
        """
        return request.method == wanted_method

    @staticmethod
    def __responseIfMethodNotAvailable():
        """
        Returns a HTTP 405 Method Not Allowed response.

        This function is typically used as a fallback response when a client
        tries to use an HTTP method that is not supported by the server for a
        particular resource.

        Returns:
            Response: A Response object with a status code of 405 
                        => (Method Not Allowed).
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @staticmethod
    def __responseIfNotAllowed():
        Response(status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def __responseIfAlright():
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def __reduceDictWithKeyList(
        dict_to_reduce: dict,
        wanted_key_list: list
    ) -> dict:
        def filter_function(key_value_pair):
            key, _ = key_value_pair
            return key in wanted_key_list

        if wanted_key_list is None or dict_to_reduce is None:
            return dict_to_reduce

        return dict(filter(
            filter_function,
            dict_to_reduce.items()
        ))

    @staticmethod
    def __getRequestInfos(
        request: HttpRequest
    ) -> dict:
        query_params = GeneralInfo.queryParamsIntoDict(request)
        request_data = request.data
        request_user_id = request.user.id

        return {
            "query_params": query_params,
            "request_data": request_data,
            "request_user_id": request_user_id
        }
    
    @classmethod
    def __checkGeneralInfoIsProperlyConfigured(cls):
        if not (
            hasattr(cls, 'base_url') and
            hasattr(cls, 'allowed_method_list') and
            hasattr(cls, 'required_permission_list')
        ):
            raise Exception('GeneralInfo not properly configured')

    @staticmethod
    def queryParamsIntoDict(request):
        return {
            key: json.loads(value)
            for key, value in request.query_params.dict().items()
        }
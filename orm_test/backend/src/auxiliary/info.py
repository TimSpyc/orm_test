import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.src.auxiliary.manager import GeneralManager
from backend.src.auxiliary.new_cache import CacheHandler
from django.urls import path
from django.http.request import HttpRequest
from backend.src.auxiliary.exceptions import *
import json
from backend.src.auxiliary.timing import timeit
from django.conf import settings
from datetime import datetime

from backend.src.auxiliary.new_cache import CacheHandler


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
        f'{prefix}__{key}': value
        for key, value in dictionary.items()
    }


class GeneralInfo:
    """
        Abstract class for handling requests, responses and define urls.
        Requests could handle the following query parameters:
            attributes: list of attributes to be returned
                (default: all attributes)
            search: string to be searched in search key attributes
                (default: None)
            search_keys: list of keys to be searched
                (default: all keys)
            sort_by: string to sort the results (e.g. "key:order")
            page: int to select the page (default: 1)
            page_size: int to select the page size (default: all results)
            filter: dict to filter on db level (e.g. {"key": "value"})
            group_by: list of keys to group by (e.g. ["key1", "key2"])

        Attributes:
            base_url: str => url to be used in urls.py (e.g. 'example')
            allowed_method_list: list => list of allowed methods
                (['GET_list', 'POST', 'GET_detail', 'PUT', 'DELETE'])
            required_permission_list: list => list of required permissions
                (not implemented yet)
            detail_key_dict: dict => dict of key and key_type for detail url
                (e.g. {'group_id': 'int'})
            manager (OPTIONAL): GeneralManager => manager to be used for
                requests if not set you need to define the following functions:
                    getList: function => function to get list of objects
                        (used for method 'GET_list')
                    getDetail: function => function to get detail of object
                        (used for method 'GET_detail')
                    create: function => function to create object
                        (used for method 'POST')
                    update: function => function to update object
                        (used for method 'PUT')
                    deactivate: function => function to deactivate object
                        (used for method 'DELETE')
            datasetPermissionFunction (OPTIONAL): function => function to
                check if dataset is allowed to be sent. Needs to return True if
                allowed, False if not. (e.g. lambda data_set_dict: True)
            serializerFunction (OPTIONAL): function => function to serialize
                data (e.g. lambda data_object : {'key': data_object.key})

        Simple Example:
            class ExampleInfo(GeneralInfo):
                base_url = 'example'
                allowed_method_list = ['GET_list', 'POST', 'GET_detail']
                required_permission_list = ['example_permission']
                detail_key_dict = {'group_id': 'int'}
                manager = ExampleManager
    """
    WITHOUT_IDENTIFIER_OPERATIONS = {'GET_list', 'POST'}
    WITH_IDENTIFIER_OPERATIONS = {'GET_detail', 'PUT', 'DELETE'}

    base_url: str
    allowed_method_list: list # ['GET_detail', 'GET_list', 'POST', 'PUT', 'DELETE']
    required_permission_list: list
    detail_key_dict: dict = {'group_id': 'int'}

    manager: "GeneralManager" # Optional
    datasetPermissionFunction = lambda data_set_dict: True
    serializerFunction = lambda data_object : dict(data_object)
    use_cache = True

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.use_cache = settings.USE_CACHE and instance.use_cache
        return instance

    def __init__(
        self,
        request:HttpRequest,
        request_type: str,
        **identifier: dict
    ):
        self.__checkGeneralInfoIsProperlyConfigured()
        if request_type not in ['detail', 'list']:
            raise ValueError('type must be "detail" or "list"')
        self.request = request
        self.type = request_type
        self.method = request.method

        self.request_response_dict = {
            ('GET', 'list'): self.__handleGetList,
            ('POST', 'list'): self.post,
            ('GET', 'detail'): self.__handleGetDetail,
            ('PUT', 'detail'): self.put,
            ('DELETE', 'detail'): self.delete
        }

        self.request_info_dict = self.__getRequestInfos()
        filter_params = self.request_info_dict["query_params"].get('filter', {})
        self._identification_dict = {
            **filter_params,
            'base_url': self.base_url
        }
        self.identifier = identifier
        self._dependencies = []

    @catchErrorsAndAdjustResponse
    def respond(self) -> list | dict | int:
        selection = (self.method, self.type)
        if selection in self.request_response_dict:
            return self.request_response_dict[selection]()
        else:
            return self.__responseIfMethodNotAvailable()

    def getDetail(self) -> "GeneralManager":
        search_date = self.request_info_dict['query_params'].get(
            'search_date',
            None
        )
        return self.manager(
            search_date=search_date,
            **self.identifier,
        )

    def put(self) -> None:
        self.__checkConfiguration()

        # manager_obj = self.manager(
        #     self.identifier['group_id'],
        #     self.request_info_dict['request_data']['creation_date']
        # )
        
        # manager_obj.update(
        #         creator_id = self.request_info_dict["request_user_id"],
        #         **self.request_info_dict['request_data']
        #     )


        manager_obj = self.manager(
            self.identifier['group_id'],
        )
        
        manager_obj.update(
                creator_id = 1,
                **self.request_info_dict['request_data']
            )

    def delete(self) -> None:
        self.__checkConfiguration()

        manager_obj = self.manager(
            self.identifier['group_id'],
            self.request_info_dict['request_data']['creation_date']
        )
        
        manager_obj.deactivate(
                creator_id = self.request_info_dict["request_user_id"],
            )

    def getList(self) -> list[object]:
        search_date = self.request_info_dict['query_params'].get(
            'search_date',
            None
        )
        filter_dict = self.request_info_dict['query_params'].get('filter', {})

        return self.manager.filter(
            search_date=search_date,
            **filter_dict,
        )

    def post(self) -> int:
        self.__checkConfiguration()

        manager_obj = self.manager.create(
            creator_id = self.request_info_dict["request_user_id"],
            **self.request_info_dict['request_data']
        )

        return manager_obj.group_id

    def __getCacheData(self) -> 'GeneralInfo':
        if self.use_cache:
            return CacheHandler.getObjectFromCache(self._identification_dict)
        else:
            return None

    def __setCacheData(self) -> None:
        CacheHandler.addDependentObjectToCache(
            self._dependencies,
            self,
            self.result_list_dict
        )

    def _updateCache(self) -> None:
        if self.use_cache:
            self.__getNewResultDict()

    def __getNewResultDict(self) -> dict:
        object_list = self.getList()
        self.result_list_dict = list(map(
            lambda manager_obj: self.__serializeData(manager_obj),
            object_list
        ))
        self.__setCacheData()
        return self.result_list_dict

    def __checkConfiguration(self) -> None:
        has_manager = hasattr(self, 'manager')
        is_manager = issubclass(self.manager, GeneralManager)

        if not has_manager or not is_manager:
            raise Exception('manager not found')
    
    def __serializeData(
        self,
        data_object: object
    ) -> dict:
        return self.__class__.serializerFunction(data_object)

    @timeit
    def __handleGetList(self) -> list[dict]:
        result_list_dict = self.__getCacheData()
        if not result_list_dict:
            result_list_dict = self.__getNewResultDict()
        result_list_dict = self.__reduceGetResultList(result_list_dict)
        result_list_dict = self.__search(result_list_dict)
        result_list_dict = self.__groupBy(result_list_dict)
        result_list_dict = self.__sort(result_list_dict)
        return self.__paginate(result_list_dict)

    def __groupBy(self, result_list_dict: list[dict]) -> list[dict]:
        group_by = self.request_info_dict['query_params'].get(
            'group_by',
            None
        )

        if group_by is None:
            return result_list_dict
        self.__checkGroupByFormat(group_by, result_list_dict)
        
        level_1_list, level_2_dict = self.__getGroupLevelDict(group_by)
        grouped_data = self.__buildGroups(result_list_dict, level_1_list)
        return self.__combineData(grouped_data, level_1_list, level_2_dict)

    def __checkGroupByFormat(
        self,
        group_by: list[str],
        result_list_dict: list[dict]
    ) -> None:
        if type(group_by) is not list:
            raise ValueError('group_by must be a list of strings')
        for group in group_by:
            if type(group) is not str:
                raise ValueError('group_by must be a list of strings')
            group_list = group.split('.')
            if len(group_list) > 2:
                raise Exception("Group by is not supported for more than 2 levels")
            if group_list[0] not in result_list_dict[0].keys():
                raise Exception(f"Group by key {group_list[0]} not found")

    @staticmethod
    def __getGroupLevelDict(group_by: list[str]) -> list[str]:
        group_level_dict = {}
        for group in group_by:
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

    @staticmethod
    def __buildGroups(data, group_by):
        groups = {}
        for item in data:
            key = tuple([item[key] for key in group_by])
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups

    def __combineData(self, data, level_1_list, level_2_dict):
        output_data = []
        for group_data_list in data.values():    
            list_for_combined_data = self.__buildListForToCombineData(group_data_list)
            combined_data = self.__combineGroupedData(list_for_combined_data, level_1_list, level_2_dict)
            output_data.append(combined_data)
        return output_data

    @staticmethod
    def __buildListForToCombineData(group_data_list):
        combined_data = {}
        for data in group_data_list:
            for key, value in data.items():
                if key not in combined_data:
                    combined_data[key] = []
                combined_data[key].append(value)
        return combined_data

    def __combineGroupedData(self, combined_data, level_1_list, level_2_dict):
        group_by = level_1_list
        for key, value in combined_data.items():
            if "_id" in key:
                value = [str(x) for x in set(value)]
            if key in group_by:
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
                    combined_data[key] = self.__combineData(
                        self.__buildGroups(combined_data[key], level_2_dict[key]),
                    level_2_dict[key], [])
            elif all(isinstance(x, datetime) for x in value):
                combined_data[key] = max(value)
            else:
                raise Exception(f"Cannot combine {key} with values {value}")
        return combined_data

    def __sort(self, result_list_dict: list[dict]) -> list[dict]:
        sort_by = self.request_info_dict['query_params'].get(
            'sort_by',
            None
        )
        if sort_by is None:
            return result_list_dict

        sort_key, sort_order = sort_by.split(':')
        if sort_key not in result_list_dict[0].keys():
            raise ValueError(f'key "{sort_key}" not found')
        if sort_order == 'asc':
            reverse = False
        elif sort_order == 'desc':
            reverse = True
        else:
            raise ValueError('sort_order must be "asc" or "desc"')
        
        def sortFunction(dict_item: dict) -> any:
            return str(dict_item[sort_key])
        return sorted(result_list_dict, key=sortFunction, reverse=reverse)

    def __search(self, result_list_dict: list[dict]) -> list[dict]:
        search_string = self.request_info_dict['query_params'].get(
            'search',
            None
        )
        if search_string is None:
            return result_list_dict
        search_string = search_string.lower()
        search_word_list = search_string.split(' ')

        search_keys = self.request_info_dict['query_params'].get(
            'search_keys',
            result_list_dict[0].keys()
        )

        def searchFunction(dict_item: dict) -> bool:
            search_text = ' '.join([
                str(dict_item.get(key, ''))
                for key in search_keys
            ]).lower()
            is_found = True
            for word in search_word_list:
                if word not in search_text:
                    is_found = False
                    break
            return is_found

        return list(filter(searchFunction, result_list_dict))

    def __paginate(self, result_list_dict: list[dict]) -> list[dict]:
        page = self.request_info_dict['query_params'].get(
            'page',
            1
        )
        page_size = self.request_info_dict['query_params'].get(
            'page_size',
            None
        )
        if page_size is None:
            return {
                "data": result_list_dict,
                "page":{'current': 1, 'max': 1}
            }
        
        start_index = (page - 1) * page_size
        end_index = page * page_size
        page_count = len(result_list_dict) // page_size
        if len(result_list_dict) % page_size != 0:
            page_count += 1

        return ({
            "data": result_list_dict[start_index:end_index], 
            "page": {'current': page, 'max': page_count}
        })

    def __handleGetDetail(self) -> dict:
        manager_obj = self.getDetail()
        result_dict = self.__serializeData(manager_obj)
        return self.__reduceGetResult(result_dict)

    def __reduceGetResult(
        self,
        result_dict: dict,
    ) -> dict:
        attributes = self.request_info_dict['query_params'].get(
            'attributes',
            None
        )
        if self.__couldBeSend(result_dict):
            return self.__reduceDictWithKeyList(result_dict, attributes)

    def __reduceGetResultList(
        self,
        result_list: list[dict],
    ) -> list[dict]:
        attributes = self.request_info_dict['query_params'].get(
            'attributes',
            None
        )

        filtered_and_reduced_list = list(map(
            lambda dict_keys: self.__reduceDictWithKeyList(
                dict_keys,
                attributes
            ), filter(lambda item: self.__couldBeSend(item), result_list)
        ))
        return filtered_and_reduced_list

    def __couldBeSend(self, result_dict: dict) -> bool:
        return self.__class__.datasetPermissionFunction(result_dict)

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
    def __getRequestFunction(cls, type:str):
        if type == 'detail':
            allowed_detail_methods = cls.__getAllowedMethodsList('detail')

            @api_view(allowed_detail_methods)
            def detailRequest(request: HttpRequest, **identifier: dict) -> Response:
                return cls.__handleRequest(request, 'detail', **identifier)
            return detailRequest

        elif type == 'list':
            allowed_list_methods = cls.__getAllowedMethodsList('list')

            @api_view(allowed_list_methods)
            def listRequest(request: HttpRequest) -> Response:
                return cls.__handleRequest(request, 'list')
            return listRequest

        else:
            raise ValueError('type must be "detail" or "list"')
    
    @classmethod
    def getUrlList(cls) -> list:
        allowed_model_operations = set(cls.allowed_method_list)

        url_list = []

        if cls.WITHOUT_IDENTIFIER_OPERATIONS & allowed_model_operations:
            url_list.append(path(
                f'{cls.base_url}/',
                cls.__getRequestFunction('list')
            ))
        if cls.WITH_IDENTIFIER_OPERATIONS & allowed_model_operations:
            identifier_string = '/'.join([
                f'<{key_type}:{key}>'
                for key, key_type in cls.detail_key_dict.items()
            ])

            url_list.append(path(
                f'{cls.base_url}/{identifier_string}',
                cls.__getRequestFunction('detail')
            ))

        return url_list

    @classmethod
    def __handleRequest(
        cls,
        request: HttpRequest,
        request_type: str,
        **identifier: dict
    ) -> list | dict | int:
        cls.__checkIfUserIsAuthorized(request)
        return cls(request, request_type, **identifier).respond()

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

    def __getRequestInfos(self) -> dict:
        query_params = self.queryParamsIntoDict(self.request)
        request_data = self.request.data
        request_user_id = self.request.user.id

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

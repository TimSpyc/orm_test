from celery import shared_task
from backend.src.auxiliary.websocket import ApiRequestConsumer
from requests import request
import json
import copy

@shared_task
def taskForCacheInvalidation(identification_dict):
    url = getUrlOutOfInfoIdentificationDict(
        identification_dict
    )
    request('GET', url)
    ApiRequestConsumer.letClientsRefetch(identification_dict)    


def getUrlOutOfInfoIdentificationDict(identification_dict):
    filter_dict = copy.deepcopy(identification_dict)
    filter_dict.pop('base_url')
    filter_str = json.dumps(filter_dict, sort_keys=True)
    url = f'http://daphne:8001/api/{identification_dict["base_url"]}/?filter={filter_str}'
    return url
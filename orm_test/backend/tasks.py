from celery import shared_task
from backend.src.auxiliary.websocket import ApiRequestConsumer
from requests import request
import json
import copy

def informWorkerToRefreshCache(info_object):
    url = getUrlOutOfInfoIdentificationDict(
        info_object.request,
        info_object._identification_dict
    )
    identification_dict = info_object._identification_dict
    taskForCacheInvalidation.delay(identification_dict, url)


@shared_task
def taskForCacheInvalidation(identification_dict, url):
    request('GET', url)
    ApiRequestConsumer.letClientsRefetch(identification_dict)    


def getUrlOutOfInfoIdentificationDict(request, identification_dict):
    host = request._request.headers['host']
    filter_dict = copy.deepcopy(identification_dict)
    filter_dict.pop('base_url')
    filter_str = json.dumps(filter_dict, sort_keys=True)
    url = f'{host}/api/{identification_dict["base_url"]}/?filter={filter_str}'
    return url
from celery import shared_task
from backend.src.auxiliary.websocket import ApiRequestConsumer
from backend.src.auxiliary.info import getUrlOutOfInfoIdentificationDict
from requests import request

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
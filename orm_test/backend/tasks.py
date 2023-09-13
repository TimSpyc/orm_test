from celery import shared_task
from backend.src.auxiliary.websocket import ApiRequestConsumer

@shared_task
def informWorkerToRefreshCache(info_object):
    info_object._updateCache()
    ApiRequestConsumer.letClientsRefetch(info_object._identification_dict)

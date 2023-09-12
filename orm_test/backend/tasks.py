from celery import shared_task
from backend.src.auxiliary.websocket import ApiRequestConsumer

def informWorkerToRefreshCache(info_object):

    @shared_task
    def refreshCache() -> None:
        info_object._updateCache()
        ApiRequestConsumer.letClientsRefetch(info_object._identification_dict)

    refreshCache.delay()
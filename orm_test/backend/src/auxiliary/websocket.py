import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from hashlib import md5

from urllib.parse import urlparse, parse_qs

def extractBaseUrlAndFilter(url:str) -> (str, dict):
    parsed_url = urlparse(url)
    base_url = '/'.join(parsed_url.path.rstrip('/').split('/')[2:])
    query_params = parse_qs(parsed_url.query)
    filter_dict = {}
    filter_str = query_params.get('filter', [None])[0]
    if filter_str:
        try:
            filter_dict = json.loads(filter_str)
        except json.JSONDecodeError:
            pass
    return base_url, filter_dict

class ApiRequestConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def receive(self, text_data):
        text_data = json.loads(text_data)
        message_type = text_data['type']
        if message_type == 'register_url':
            base_url, filter_dict = extractBaseUrlAndFilter(text_data['url'])
            _identification_dict = {
                **filter_dict,
                'base_url': base_url
            }
            id_string = json.dumps(_identification_dict, sort_keys=True)
            url_hash = md5(id_string.encode()).hexdigest()
            async_to_sync(self.channel_layer.group_add)(
                url_hash,
                self.channel_name
            )

    @classmethod
    def letClientsRefetch(cls, _identification_dict):
        """
        inform all connected clients that the cache for the given url should be
        invalidated and re-fetched.
        """
        channel_layer = get_channel_layer()
        id_string = json.dumps(_identification_dict, sort_keys=True)
        url_hash = md5(id_string.encode()).hexdigest()
        async_to_sync(channel_layer.group_send)(
            url_hash, {
                'type': 'send_update_cache',
                'message': {
                    "type": "refetch",
                    "url": id_string
                },
            }
        )

    def send_update_cache(self, event):
        self.send(text_data=json.dumps(event['message']))

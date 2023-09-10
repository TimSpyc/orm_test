import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from hashlib import md5

url_list = []

class ApiRequestConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'message': 'connected'
        }))

    def receive(self, text_data):
        print('received', text_data)
        text_data = json.loads(text_data)
        message_type = text_data['type']
        if message_type == 'register_url':
            print(text_data['url'])

            url = md5(text_data['url'].encode()).hexdigest()
            async_to_sync(self.channel_layer.group_add)(
                url,
                self.channel_name
            )
            if url not in url_list:
                url_list.append(url)
            self.send(text_data=json.dumps({
                'message': 'registered',
                'url_list': url_list
            }))

    def disconnect(self, close_code):
        print('disconnected', close_code)
        pass

    @classmethod
    def sendToAllConsumers(cls, url):
        """
        Informiert alle Verbraucher, die sich für die URL registriert haben.
        """
        # Wir holen das Channel Layer
        channel_layer = get_channel_layer()

        # Die URL in ein md5 Hash konvertieren, um die Gruppe zu erhalten
        url_hash = md5(url.encode()).hexdigest()

        # Senden Sie die Nachricht an alle Verbraucher, die sich für diese URL registriert haben.
        async_to_sync(channel_layer.group_send)(
            url_hash, {
                'type': 'send_notification',
                'message': "refetch"
            }
        )

    # Dies ist der Handler für die 'send_notification' Nachrichtentyp
    def send_notification(self, event):
        # Sendet die Nachricht an den Client über WebSockets
        self.send(text_data=json.dumps(event['message']))

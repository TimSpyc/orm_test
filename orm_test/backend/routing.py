from django.urls import re_path
from backend.src.auxiliary.websocket import ApiRequestConsumer
websocket_urlpatterns = [
    re_path(r'ws/cache_invalidator/', ApiRequestConsumer.as_asgi()),
]

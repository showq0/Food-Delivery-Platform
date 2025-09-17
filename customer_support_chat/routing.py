from django.urls import re_path
from .consumers import MessagesConsumer

websocket_urlpatterns = [
    re_path(r'ws/messages/(?P<chat_id>\d+)/$', MessagesConsumer.as_asgi()),
]
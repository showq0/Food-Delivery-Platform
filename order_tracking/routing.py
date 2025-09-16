from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/track-location/(?P<order_id>\d+)/$', consumers.TrackConsumer.as_asgi()),
]

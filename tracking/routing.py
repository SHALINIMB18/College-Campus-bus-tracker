from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/live-tracking/(?P<route_number>\w+)/$', consumers.LiveTrackingConsumer.as_asgi()),
    re_path(r'ws/driver-location/(?P<driver_id>\d+)/$', consumers.DriverLocationConsumer.as_asgi()),
]

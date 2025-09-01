from django.urls import path
from .views import update_location, live_tracking, driver_live_map, get_live_locations, get_route_details

urlpatterns = [
    path('update/', update_location, name='update_location'),
    path('live/', live_tracking, name='live_tracking'),
    path('driver/live/', driver_live_map, name='driver_live_map'),
    path('api/live_locations/', get_live_locations, name='get_live_locations'),
    path('api/route_details/<str:route_number>/', get_route_details, name='get_route_details'),
]

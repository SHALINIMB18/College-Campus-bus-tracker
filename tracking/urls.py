from django.urls import path
from .views import update_location, live_tracking

urlpatterns = [
    path('update/', update_location, name='update_location'),
    path('live/', live_tracking, name='live_tracking'),
]

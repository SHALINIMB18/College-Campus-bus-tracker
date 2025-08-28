from django.urls import path
from .views import route_search

urlpatterns = [
    path('search/', route_search, name='route_search'),
]

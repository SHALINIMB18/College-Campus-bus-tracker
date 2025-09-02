
from django.contrib import admin
from .models import BusRoute, BusStop

@admin.register(BusRoute)
class BusRouteAdmin(admin.ModelAdmin):
	list_display = ('route_number', 'timings')

@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ('name', 'route', 'latitude', 'longitude')

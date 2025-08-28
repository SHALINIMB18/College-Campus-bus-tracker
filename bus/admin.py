
from django.contrib import admin
from .models import BusRoute, Assignment

@admin.register(BusRoute)
class BusRouteAdmin(admin.ModelAdmin):
	list_display = ('route_number', 'timings')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
	list_display = ('bus_route', 'driver')

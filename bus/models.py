

from django.db import models
from users.models import User

class BusRoute(models.Model):
	route_number = models.CharField(max_length=20, unique=True)
	stops = models.TextField(help_text='Comma-separated list of stops')
	timings = models.CharField(max_length=100)

	def __str__(self):
		return f"Route {self.route_number}"

class Assignment(models.Model):
	bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
	driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_routes')
	students = models.ManyToManyField(User, related_name='student_routes', blank=True)
	staff = models.ManyToManyField(User, related_name='staff_routes', blank=True)

	def __str__(self):
		return f"Assignment for {self.bus_route}"

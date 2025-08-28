

from django.db import models
from bus.models import BusRoute
from users.models import User

class Location(models.Model):
	bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
	driver = models.ForeignKey(User, on_delete=models.CASCADE)
	latitude = models.FloatField()
	longitude = models.FloatField()
	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.bus_route} - {self.driver} @ {self.timestamp}"

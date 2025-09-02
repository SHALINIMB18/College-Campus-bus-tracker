from django.db import models

class BusRoute(models.Model):
    route_number = models.CharField(max_length=10, unique=True)
    timings = models.CharField(max_length=100, blank=True)
    stops = models.TextField(blank=True)  # Comma-separated stop names

    def __str__(self):
        return self.route_number

class Assignment(models.Model):
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    driver = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.driver} assigned to {self.bus_route}"

class BusStop(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    route = models.ForeignKey(BusRoute, related_name='bus_stops', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.route.route_number})"

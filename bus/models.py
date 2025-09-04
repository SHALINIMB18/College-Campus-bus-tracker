from django.db import models
from django.conf import settings

class BusRoute(models.Model):
    route_number = models.CharField(max_length=10, unique=True)
    timings = models.CharField(max_length=100, blank=True)
    stops = models.TextField(blank=True)  # Comma-separated stop names

    def __str__(self):
        return self.route_number

class Assignment(models.Model):
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    driver = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ManyToManyField(blank=True, related_name='staff_routes', to=settings.AUTH_USER_MODEL)
    students = models.ManyToManyField(blank=True, related_name='student_routes', to=settings.AUTH_USER_MODEL)

    def __str__(self):
        return f"{self.driver} assigned to {self.bus_route}" if self.driver else f"Assignment for {self.bus_route}"

class BusStop(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    route = models.ForeignKey(BusRoute, related_name='bus_stops', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.route.route_number})"

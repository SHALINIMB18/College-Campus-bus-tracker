

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	ROLE_CHOICES = [
		('student', 'Student'),
		('staff', 'Staff'),
		('driver', 'Driver'),
		('admin', 'Admin'),
	]
	full_name = models.CharField(max_length=100)
	phone = models.CharField(max_length=20, unique=True)
	role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

	def __str__(self):
		return f"{self.full_name} ({self.role})"

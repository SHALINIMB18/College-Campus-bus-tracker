from django import forms
from .models import Location

class LocationUpdateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['bus_route', 'latitude', 'longitude']

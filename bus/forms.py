from django import forms
from .models import BusRoute

class RouteSearchForm(forms.Form):
    query = forms.CharField(label='Search Bus Route', max_length=100, required=False)

class BusRouteForm(forms.ModelForm):
    class Meta:
        model = BusRoute
        fields = ['route_number', 'stops', 'timings']

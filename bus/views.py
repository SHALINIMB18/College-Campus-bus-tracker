from django.shortcuts import render
from .models import BusRoute
from .forms import RouteSearchForm

def route_search(request):
    form = RouteSearchForm(request.GET or None)
    routes = BusRoute.objects.all()
    if form.is_valid() and form.cleaned_data['query']:
        q = form.cleaned_data['query']
        routes = routes.filter(route_number__icontains=q)
    return render(request, 'bus/route_search.html', {'form': form, 'routes': routes})

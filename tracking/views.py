from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Location
from .forms import LocationUpdateForm
from bus.models import BusRoute
from bus.notifications import notify_users_on_bus_active


@login_required
def update_location(request):
    if request.method == 'POST':
        form = LocationUpdateForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.driver = request.user
            location.save()
            # Send notification to users on this route
            eta = 'N/A'  # Placeholder, can be calculated with Google Maps API
            notify_users_on_bus_active(location.bus_route.route_number, eta, request.user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok'})
            return redirect('dashboard')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = LocationUpdateForm()
    return render(request, 'tracking/update_location.html', {'form': form})

@login_required
def live_tracking(request):
    routes = BusRoute.objects.all()
    selected_route = request.GET.get('route')
    locations = Location.objects.filter(bus_route__route_number=selected_route) if selected_route else []
    return render(request, 'tracking/live_tracking.html', {'routes': routes, 'locations': locations, 'selected_route': selected_route})

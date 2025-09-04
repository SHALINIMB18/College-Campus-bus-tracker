from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.utils import timezone
from datetime import timedelta

from .models import Location
from .forms import LocationUpdateForm
from bus.models import BusRoute, Assignment
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

@login_required
def driver_live_map(request):
    """Driver-specific live map showing assigned route and location sharing controls"""
    if request.user.role != 'driver':
        return redirect('dashboard')

    # Get driver's assigned routes
    assignments = Assignment.objects.filter(driver=request.user)
    if not assignments.exists():
        return render(request, 'tracking/driver_live_map.html', {
            'error': 'No routes assigned to you. Please contact administrator.'
        })

    # Get the first assigned route (could be enhanced to handle multiple routes)
    assignment = assignments.first()
    bus_route = assignment.bus_route

    # Parse stops from the route
    stops = [stop.strip() for stop in bus_route.stops.split(',')] if bus_route.stops else []

    # Get recent locations for this route
    recent_locations = Location.objects.filter(
        bus_route=bus_route,
        timestamp__gte=timezone.now() - timedelta(minutes=5)
    ).order_by('-timestamp')

    # Check if driver is currently sharing location
    is_sharing = recent_locations.filter(driver=request.user).exists()

    return render(request, 'tracking/driver_live_map_clean.html', {
        'bus_route': bus_route,
        'stops': stops,
        'recent_locations': recent_locations,
        'is_sharing': is_sharing
    })

@login_required
def get_live_locations(request):
    """API endpoint to get live locations for a specific route"""
    route_number = request.GET.get('route')
    if not route_number:
        return JsonResponse({'error': 'Route number required'}, status=400)
    
    # Get locations from last 5 minutes
    recent_locations = Location.objects.filter(
        bus_route__route_number=route_number,
        timestamp__gte=timezone.now() - timedelta(minutes=5)
    ).select_related('driver', 'bus_route').order_by('-timestamp')
    
    locations_data = []
    for loc in recent_locations:
        locations_data.append({
            'driver': loc.driver.full_name,
            'route': loc.bus_route.route_number,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'timestamp': loc.timestamp.isoformat(),
            'is_active': (timezone.now() - loc.timestamp).total_seconds() < 60  # Active if updated in last minute
        })
    
    return JsonResponse({'locations': locations_data})

@login_required
def get_route_details(request, route_number):
    """API endpoint to get route details including stops"""
    bus_route = get_object_or_404(BusRoute, route_number=route_number)
    # Use BusStop model to get stops with lat/lng
    stops_qs = bus_route.bus_stops.all()
    stops = []
    for stop in stops_qs:
        stops.append({
            'name': stop.name,
            'latitude': stop.latitude,
            'longitude': stop.longitude
        })
    
    return JsonResponse({
        'route_number': bus_route.route_number,
        'timings': bus_route.timings,
        'stops': stops
    })

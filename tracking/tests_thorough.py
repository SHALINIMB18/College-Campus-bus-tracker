from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from bus.models import BusRoute, Assignment
from tracking.models import Location
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TrackingThoroughTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass', role='driver')
        self.bus_route = BusRoute.objects.create(route_number='R1', stops='Stop1, Stop2', timings='9AM-5PM')
        self.assignment = Assignment.objects.create(driver=self.user, bus_route=self.bus_route)

    def test_driver_live_map_requires_login(self):
        response = self.client.get(reverse('driver_live_map'))
        self.assertRedirects(response, f'/users/login/?next={reverse("driver_live_map")}')

    def test_driver_live_map_access(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('driver_live_map'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/driver_live_map_clean.html')

    def test_get_live_locations_api(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('get_live_locations'), {'route': self.bus_route.route_number})
        self.assertEqual(response.status_code, 200)
        self.assertIn('locations', response.json())

    def test_get_route_details_api(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('get_route_details', args=[self.bus_route.route_number]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['route_number'], self.bus_route.route_number)

    def test_update_location_post_invalid(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'bus_route': '',  # Missing bus_route
            'latitude': 12.34,
            'longitude': 56.78,
        }
        response = self.client.post(reverse('update_location'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())

    def test_live_tracking_with_route(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('live_tracking'), {'route': self.bus_route.route_number})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.bus_route.route_number)

    def test_location_is_active_flag(self):
        self.client.login(username='testuser', password='testpass')
        # Create a recent location
        Location.objects.create(
            driver=self.user,
            bus_route=self.bus_route,
            latitude=12.34,
            longitude=56.78,
            timestamp=timezone.now()
        )
        response = self.client.get(reverse('get_live_locations'), {'route': self.bus_route.route_number})
        locations = response.json().get('locations', [])
        self.assertTrue(any(loc['is_active'] for loc in locations))

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from bus.models import BusRoute
from tracking.models import Location

User = get_user_model()

class TrackingCriticalPathTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.bus_route = BusRoute.objects.create(route_number='R1', stops='Stop1, Stop2', timings='9AM-5PM')

    def test_live_tracking_requires_login(self):
        response = self.client.get(reverse('live_tracking'))
        self.assertRedirects(response, f'/users/login/?next={reverse("live_tracking")}')

    def test_update_location_requires_login(self):
        response = self.client.get(reverse('update_location'))
        self.assertRedirects(response, f'/users/login/?next={reverse("update_location")}')

    def test_live_tracking_page(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('live_tracking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/live_tracking.html')

    def test_update_location_page_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('update_location'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/update_location.html')

    def test_update_location_post(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'bus_route': self.bus_route.id,
            'latitude': 12.34,
            'longitude': 56.78,
        }
        response = self.client.post(reverse('update_location'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful post
        self.assertTrue(Location.objects.filter(driver=self.user, bus_route=self.bus_route).exists())

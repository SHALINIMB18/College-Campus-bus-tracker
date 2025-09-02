from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from bus.models import Assignment
import random

User = get_user_model()

class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create users with different roles
        self.driver = User.objects.create_user(username='driver1', password='pass', role='driver', phone=f'1000000000{random.randint(1,9999)}')
        self.student = User.objects.create_user(username='student1', password='pass', role='student', phone=f'2000000000{random.randint(1,9999)}')
        self.staff = User.objects.create_user(username='staff1', password='pass', role='staff', phone=f'3000000000{random.randint(1,9999)}')
        self.admin = User.objects.create_user(username='admin1', password='pass', role='admin', phone=f'4000000000{random.randint(1,9999)}')

        # Create a bus route for assignment
        from bus.models import BusRoute
        self.bus_route = BusRoute.objects.create(route_number='R1', timings='9AM-5PM', stops='Stop1,Stop2')

        # Create assignments for driver
        self.assignment1 = Assignment.objects.create(driver=self.driver, bus_route=self.bus_route)

    def test_dashboard_driver(self):
        self.client.login(username='driver1', password='pass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('assignments' in response.context)
        self.assertTrue(response.context['is_driver'])
        self.assertIn(self.assignment1, response.context['assignments'])

    def test_dashboard_student(self):
        self.client.login(username='student1', password='pass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('assignments' in response.context)
        self.assertFalse(response.context.get('is_driver', True))

    def test_dashboard_staff(self):
        self.client.login(username='staff1', password='pass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('assignments' in response.context)
        self.assertFalse(response.context.get('is_driver', True))

    def test_dashboard_admin(self):
        self.client.login(username='admin1', password='pass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('is_admin', False))

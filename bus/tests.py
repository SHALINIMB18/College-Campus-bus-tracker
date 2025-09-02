from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from bus.models import BusRoute, Assignment
from bus.notifications import notify_users_on_bus_active

User = get_user_model()

class NotificationTests(TestCase):
    def setUp(self):
        # Create test users with unique phone numbers to avoid IntegrityError
        self.student = User.objects.create_user(username='student1', email='student1@example.com', password='pass', phone='1111111111')
        self.staff = User.objects.create_user(username='staff1', email='staff1@example.com', password='pass', phone='2222222222')
        self.driver = User.objects.create_user(username='driver1', email='driver1@example.com', password='pass', full_name='Driver One', phone='3333333333')

        # Create bus route
        self.route = BusRoute.objects.create(route_number='R1', timings='9AM-5PM')

        # Create assignment with students and staff
        self.assignment = Assignment.objects.create(bus_route=self.route, driver=self.driver)
        # The Assignment model does not have students or staff fields, so this part is removed
        # You may want to add related models or adjust the test accordingly

    def test_notify_users_on_bus_active_sends_email(self):
        notify_users_on_bus_active(self.route.route_number, '10 mins', self.driver)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Bus R1 is now active!', email.subject)
        self.assertIn('Driver One', email.body)
        # Since notify_users_on_bus_active now only sends to driver, adjust test accordingly
        self.assertIn(self.driver.email, email.to)

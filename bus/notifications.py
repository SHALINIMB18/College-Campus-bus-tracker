from django.core.mail import send_mail
from django.conf import settings
from bus.models import Assignment
from users.models import User

def notify_users_on_bus_active(route_number, eta, driver):
    try:
        assignment = Assignment.objects.get(bus_route__route_number=route_number)
        # Since Assignment model has no students or staff, notify only driver for now
        emails = [driver.email] if driver.email else []
        if emails:
            subject = f"Bus {route_number} is now active!"
            message = f"Bus {route_number} is now active.\nETA: {eta}\nDriver: {driver.full_name}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, emails, fail_silently=True)
    except Assignment.DoesNotExist:
        pass

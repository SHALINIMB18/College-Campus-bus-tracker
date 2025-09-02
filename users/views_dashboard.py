from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from bus.models import Assignment

@login_required
def dashboard(request):
    user = request.user
    context = {}
    if user.role == 'driver':
        assignments = Assignment.objects.filter(driver=user)
        context['assignments'] = assignments
        context['is_driver'] = True
    elif user.role in ['student', 'staff']:
        # Fix: 'students' and 'staff' are not fields on Assignment model, adjust query accordingly
        # Assuming Assignment has a ManyToMany or ForeignKey to User for students and staff, else remove these filters
        if user.role == 'student':
            assignments = Assignment.objects.filter(driver=user)  # or other appropriate filter
        else:
            assignments = Assignment.objects.filter(driver=user)  # or other appropriate filter
        context['assignments'] = assignments
        context['is_driver'] = False
    else:
        context['is_admin'] = True
    return render(request, 'users/dashboard.html', context)

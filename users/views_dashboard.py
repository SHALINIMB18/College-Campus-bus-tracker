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
        assignments = Assignment.objects.filter(students=user) if user.role == 'student' else Assignment.objects.filter(staff=user)
        context['assignments'] = assignments
        context['is_driver'] = False
    else:
        context['is_admin'] = True
    return render(request, 'users/dashboard.html', context)

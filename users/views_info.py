from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'users/profile.html')

def about(request):
    return render(request, 'about.html')

def bus_rules(request):
    return render(request, 'bus_rules.html')

from django.urls import path
from . import views
from .views_dashboard import dashboard
from .views_info import profile, about, bus_rules

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('about/', about, name='about'),
    path('bus-rules/', bus_rules, name='bus_rules'),
]

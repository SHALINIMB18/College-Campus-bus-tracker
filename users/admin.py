
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
	model = User
	list_display = ('username', 'full_name', 'email', 'phone', 'role', 'is_staff', 'is_active')
	fieldsets = UserAdmin.fieldsets + (
		(None, {'fields': ('full_name', 'phone', 'role')}),
	)

from django.contrib import admin
from .models import Employee
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Employee)

class ProfileInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'profile'

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'email', 'first_name', 'last_name']
    inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, CustomUserAdmin)
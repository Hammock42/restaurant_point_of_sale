from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_hired = models.DateField(auto_now_add=True)
    date_fired = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
def create_employee(sender, instance, created, **kwargs):
    if created:
        employee_profile = Employee(user=instance)
        employee_profile.save()

post_save.connect(create_employee, sender=User)
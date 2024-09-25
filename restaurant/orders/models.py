from django.db import models
from items.models import Item
from employees.models import Employee

# Create your models here.
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cashier = models.ForeignKey(Employee, related_name='orders', on_delete=models.CASCADE, default=1)
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)


    def __str__(self):
        return str(self.id)
    

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def get_total_price(self):
        return self.item.price * self.quantity
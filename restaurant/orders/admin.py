from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'updated_at', 'cashier']
    list_filter = ['created_at', 'updated_at', 'cashier']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'item', 'quantity']
    list_filter = ['order', 'item']
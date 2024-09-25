from . import views
from django.urls import path

app_name = 'orders'

urlpatterns = [
    path('add/<int:item_id>/', views.order_add, name='order_add'),
    path('', views.order_detail, name='order_detail'),
    path('remove/<int:item_id>/', views.order_item_remove, name='order_item_remove'),
    path('subtract/<int:item_id>/', views.order_subtract, name='order_subtract'),
    path('clear/', views.order_clear, name='order_clear'),
    path('create/', views.order_create, name='order_create'),
    path('receipt/', views.order_receipt_view, name='order_receipt'),
]

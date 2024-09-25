from .views import *
from django.urls import path

app_name = 'items'

urlpatterns = [
    path('menu/', menu, name='menu'),
    path('category/<slug:category_slug>/', menu, name='menu_by_category'),
    path('add/<int:item_id>/', menu, name='menu_add_to_order'),
    path('item/<int:id>/<slug:slug>/', item_detail, name='item_detail'),

]
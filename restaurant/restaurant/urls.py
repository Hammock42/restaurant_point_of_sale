from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('orders/', include('orders.urls'), name='orders'),
    path('items/', include('items.urls'), name='items'),
    path('employees/', include('employees.urls'), name='employees'),
]

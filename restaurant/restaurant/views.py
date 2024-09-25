from django.shortcuts import render
from items.models import Item
from django.contrib.auth.decorators import login_required

@login_required(login_url='employees:login')
def home(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'home.html', context)

@login_required(login_url='employees:login')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='employees:login')
def settings(request):
    return render(request, 'settings.html')
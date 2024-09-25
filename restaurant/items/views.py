from django.shortcuts import render, get_object_or_404
from .models import Item, Category
from orders.models import Order, OrderItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='employees:login')
def index(request):
    pass

@login_required(login_url='employees:login')
def menu(request, category_slug=None, item_id=None):
    category = None
    items = Item.objects.filter()
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=category)

    if item_id:
        item = get_object_or_404(Item, id=int(item_id))
        order_id = request.session.get('order_id')

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                order = Order.objects.create()
        else:
            order = Order.objects.create()
            request.session['order_id'] = order.id

        item = get_object_or_404(Item, id=item_id)

        order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
        if not created:
            order_item.quantity += 1

        order_item.save()

    return render(request, 'items/menu.html', {'category': category, 'categories': categories, 'items': items})

@login_required(login_url='employees:login')
def item_detail(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug)
    return render(request, 'items/item_detail.html', {'item': item})


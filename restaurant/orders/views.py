from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem
from items.models import Item
from employees.models import Employee
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from datetime import datetime
import io
#from .print_receipt import printReceipt

# Create your views here.
@require_POST
def order_create(request):
    payment_values = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    user = get_object_or_404(Employee, id=request.user.id)
    order = Order.objects.create(cashier=user)
    order_data = request.POST.get('order_data')
    order_data = json.loads(order_data)
    for order_item in order_data:
        item = get_object_or_404(Item, id=order_item['item_id'])
        OrderItem.objects.create(order=order, item=item, quantity=order_item['item_quantity'])
    order.save()
    order_items = OrderItem.objects.filter(order=order)
    total_price = sum(item.get_total_price() for item in order_items)
    
    return render(request, 'orders/order_detail.html', {'order': order, 'order_items': order_items, 'total_price': total_price, 'payment_values': payment_values})

@require_POST
def order_add(request, item_id):
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

    response_data = {
        "success": True,
        "message": f"{item.name} added to order",
    }

    return JsonResponse(response_data)

@require_POST
def order_subtract(request, item_id):
    order_id = request.session.get('order_id')

    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(OrderItem, id=item_id, order=order)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    response_data = {
        "success": True,
        "message": f"{{item.name}} removed from order",
    }

    return JsonResponse(response_data)

@require_POST
def order_clear(request):
    order_id = request.session.get('order_id')

    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            order = Order.objects.create()
    else:
        order = Order.objects.create()
        request.session['order_id'] = order.id

    order_items = OrderItem.objects.filter(order=order)
    order_items.delete()

    response_data = {
        "success": True,
        "message": "Order cleared",
    }

    return JsonResponse(response_data)

@require_POST
def order_item_remove(request, item_id):
    order_id = request.session.get('order_id')

    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(OrderItem, id=item_id, order=order)

    item.delete()

    response_data = {
        "success": True,
        "message": f"{{item.name}} removed from order",
    }

    return JsonResponse(response_data)

def order_detail(request):
    order_id = request.session.get('order_id')
    order=None
    
    if order_id:
        order = get_object_or_404(Order, id=order_id)
    if not order or not order.items.exists():
        order = None
    
    return render(request, 'orders/order_detail.html', {'order': order})

@require_POST
def order_receipt_view(request):

    order_id = request.POST.get('order_id')
    payment_amount = float(request.POST.get('payment_amount'))
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    date = order.created_at.strftime('%Y-%m-%d %H:%M:%S')
    #printReceipt(order_id, order_items, date)
    receipt = Receipt(order, payment_amount)
    kitchen_order = KitchenOrder(order)
    return render(request, 'orders/receipt.html', {'receipt': receipt, 'kitchen_order': kitchen_order})
    

    

class Receipt:
    def __init__(self, order, payment_amount):
        self.order_id = order.id
        self.items_list = OrderItem.objects.filter(order=order)
        self.order_items = [
            {
                'item_name': item.item.name,
                'item_quantity': item.quantity,
                'item_price': item.item.price,
                'item_total_price': item.quantity * item.item.price
            }
            for item in self.items_list
        ]
        self.order_total_price = sum(item['item_total_price'] for item in self.order_items)
        self.cashier = order.cashier
        self.payment_amount = payment_amount
        self.change = self.payment_amount - float(self.order_total_price)
        self.datetime = datetime.now()

    def __str__(self):
        receipt_lines = [
            f"Pizza Shop: +218-94-6446559",
            f"Order #: {self.order_id}",
            f"Cashier: {self.cashier}",
            f"Time: {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}",
            f"--------------------------------"
        ]
        for item in self.order_items:
            receipt_lines.append(
                f"  - {item['item_name']} x {item['item_quantity']} @ {item['item_price']} each: {item['item_total_price']}"
            )
        receipt_lines.append(f"Total: {self.order_total_price}")
        receipt_lines.append(f"Payment Amount: {self.payment_amount}")
        receipt_lines.append(f"Change: {self.change}")
        return "\n".join(receipt_lines)
    
class KitchenOrder:
    def __init__(self, order):
        self.order_id = order.id
        self.items_list = OrderItem.objects.filter(order=order)
        self.order_items = [
            {
                'item_name': item.item.name,
                'item_quantity': item.quantity
            }
            for item in self.items_list
        ]
        self.datetime = datetime.now()

    def __str__(self):
        order_lines = [
            f"ORDER NUMBER: {self.order_id}",
            f"Time: {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}",
            f"--------------------------------"
        ]
        for item in self.order_items:
            order_lines.append(
                f"  - {item['item_name']} x {item['item_quantity']}"
            )
        return "\n".join(order_lines)
    

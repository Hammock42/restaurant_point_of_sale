from escpos.printer import Usb
from datetime import datetime

p = Usb(0x0483, 0x5743)
# Bus 003 Device 037: ID 0483:5743 STMicroelectronics USB Printer P

def printReceipt(order_id, order_items, date):
    p = Usb(0x0483, 0x5743)
    store_name = "Mini Pizza"

    p.set(align="center", font="a")
    p.text("Order ID: " + order_id + "\n")
    p.text('\n')
    p.set(align="left", font="a")
    p.text("{:<25} {:<5}\n".format("Item", "Qty"))
    p.text("--------------------------------------\n")
    for item in order_items:
        p.text("{:<25} x{:<5}\n".format(item["name"], item["quantity"]))
    p.cut()

    p.set(align="center", font="a")
    p.text(store_name + "\n")
    p.text(date + "\n")
    p.text("Order ID: " + order_id + "\n")
    p.text("\n")
    p.set(align="left", font="a")
    p.text("{:<20} {:<5} {:<5} {:<5}\n".format("Item", "Qty", "Price", "Total"))
    p.text("--------------------------------------\n")
    total = 0
    for item in order_items:
        total += item["price"] * item["quantity"]
        p.text("{:<20} x{:<5} {:<5.2f} {:<5.2f}\n".format(item["name"], item["quantity"], item["price"], item["price"] * item["quantity"]))
    p.text("--------------------------------------\n")
    p.text("{:<20} {:<5} {:<5} {:<5.2f}\n".format("Total", "", "", total))
    p.text("\n")
    p.set(align="center", font="a")
    p.text("Thank you for your order!\n")
    p.cut()

    p.cashdraw(2)

""" order_id = "123456"
order_items = [
    {
        "name": "Mini Tuna",
        "quantity": 2,
        "price": 2.50
    },
    {
        "name": "Soft Drink",
        "quantity": 3,
        "price": 3.00
    },
    {
        "name": "Mini Olives",
        "quantity": 1,
        "price": 1.50
    }
]

date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
printReceipt(order_id, order_items, date) """

""" from escpos.printer import Network

p = Network("127.0.0.1", 631)
p.text("Hello World\n")
p.cut() """
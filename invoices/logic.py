from orders.models import Order
from invoices.models import Invoice, InvoiceItems
from datetime import datetime, date

def create_invoice(startDate, endDate):
    startdatetime = datetime(startDate.year, startDate.month, startDate.day)
    enddatetime = datetime(endDate.year, endDate.month, endDate.day+1)

    # startdatetime = datetime.combine(startDate, datetime.min.time())
    # enddatetime = datetime.combine(endDate, datetime.max.time())
    shipped_orders = Order.objects.filter(shipDate__range=(startdatetime, enddatetime)).filter(orderStatus="Shipped")
    storenameset = set()
    for order in shipped_orders:
        if order.storeName not in storenameset:
            print('adding store', order.storeName)
            storenameset.add(order.storeName)
            invoiceno = "SFMINV-" + startDate.strftime("%m%d") + "-" + endDate.strftime("%m%d") + "-" + order.store.storeCode
            invoicenote = "invoice from SFM"
            invoice = Invoice(startDate=startDate, endDate=endDate, storeName=order.storeName, invoiceNo=invoiceno, status="Unpaid", notes=invoicenote)
        print('--order',order)
    print(shipped_orders)

def check():
    start = date(2021, 3,15)
    end = date(2021, 6, 29)
    create_invoice(start, end)
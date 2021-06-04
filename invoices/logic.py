from orders.models import Order
from products.models import Product
from invoices.models import Invoice, InvoiceItems
from datetime import datetime, date

def create_invoices(startDate, endDate):
    startdatetime = datetime(startDate.year, startDate.month, startDate.day)
    enddatetime = datetime(endDate.year, endDate.month, endDate.day+1)

    # startdatetime = datetime.combine(startDate, datetime.min.time())
    # enddatetime = datetime.combine(endDate, datetime.max.time())
    shipped_orders = Order.objects.filter(shipDate__range=(startdatetime, enddatetime)).filter(orderStatus="Shipped")
    invoice_amounts = {}

    for order in shipped_orders:
        invoiceno = "SFMINV-" + startDate.strftime("%m%d") + "-" + endDate.strftime("%m%d") \
                    + "-" + order.store.storeCode
        if invoiceno not in list(invoice_amounts.keys()):
            print('adding store', order.storeName)

            invoicenote = "invoice from SFM"
            # check if the invoice already exists, if so delete the invoice and create new
            Invoice.objects.filter(invoiceNo=invoiceno).delete()
            invoice = Invoice(startDate=startDate, endDate=endDate, storeName=order.storeName, store=order.store, invoiceNo=invoiceno,
                              status="Unpaid", notes=invoicenote, subTotal=0, discount=0, taxrate=0)
            invoice.save()
            invoice_amounts[invoiceno] = 0

        print(order.saleDate)
        invoice = Invoice.objects.get(invoiceNo=invoiceno)
        product = Product.objects.get(sfmId=order.sfmId)
        amt = product.price
        orderdate = order.saleDate if order.saleDate is not None else order.shipDate.date()
        invoiceitem = InvoiceItems(invoice=invoice, shipDate=order.shipDate.date(), orderDate=orderdate,
                                   orderNo=order.orderNo, customer=order.recipientName, description=order.sfmId,
                                   amount=amt)
        invoiceitem.save()
        invoice_amounts[invoiceno] += amt
        if order.customerPaidShipping is not None and order.customerPaidShipping > 0:
            invoiceshipitem = InvoiceItems(invoice=invoice, shipDate=order.shipDate.date(), orderDate=orderdate,
                                           orderNo=order.orderNo, customer=order.recipientName, description='Shipping',
                                           amount=order.customerPaidShipping)
            invoiceshipitem.save()
            invoice_amounts[invoiceno] += order.customerPaidShipping

    updateInvoices(invoice_amounts)
    return len(invoice_amounts)

def updateInvoices(invoice_amounts):
    invoices = Invoice.objects.filter(invoiceNo__in=list(invoice_amounts.keys()))
    for invoice in invoices:
        invoice.subTotal = invoice_amounts[invoice.invoiceNo]
        invoice.save()


def check():
    start = date(2021, 3,15)
    end = date(2021, 6, 29)
    create_invoices(start, end)
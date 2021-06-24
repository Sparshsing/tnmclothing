from decimal import Decimal

from django.template.loader import get_template

from orders.models import Order
from products.models import Product
from invoices.models import Invoice, InvoiceItems
from stores.models import Store
from datetime import datetime, date
from xhtml2pdf import pisa
from django.conf import settings

def create_invoices(startDate, endDate):
    startdatetime = datetime(startDate.year, startDate.month, startDate.day)
    enddatetime = datetime(endDate.year, endDate.month, endDate.day+1)

    # startdatetime = datetime.combine(startDate, datetime.min.time())
    # enddatetime = datetime.combine(endDate, datetime.max.time())
    shipped_orders = Order.objects.filter(shipDate__range=(startdatetime, enddatetime)).filter(orderStatus="Shipped").order_by('orderNo')
    invoice_amounts = {}
    orderNoList = []

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
        orderdate = order.saleDate if order.saleDate is not None else order.shipDate.date()
        invoice = Invoice.objects.get(invoiceNo=invoiceno)
        if order.customerPaidShipping is not None and order.customerPaidShipping > 0 and order.orderNo not in orderNoList:
            invoiceshipitem = InvoiceItems(invoice=invoice, shipDate=order.shipDate.date(), orderDate=orderdate,
                                           orderNo=order.orderNo, customer=order.recipientName, description='Shipping',
                                           amount=order.customerPaidShipping)
            invoiceshipitem.save()
            invoice_amounts[invoiceno] += order.customerPaidShipping
        orderNoList.append(order.orderNo)
        product = Product.objects.get(sfmId=order.sfmId)
        amt = product.price
        desc = order.sfmId + '-' + order.design
        invoiceitem = InvoiceItems(invoice=invoice, shipDate=order.shipDate.date(), orderDate=orderdate,
                                   orderNo=order.orderNo, customer=order.recipientName, description=desc,
                                   amount=amt)
        invoiceitem.save()
        invoice_amounts[invoiceno] += amt


    updateInvoices(invoice_amounts)
    return len(invoice_amounts)

def updateInvoices(invoice_amounts):
    invoices = Invoice.objects.filter(invoiceNo__in=list(invoice_amounts.keys()))
    for invoice in invoices:
        invoice.subTotal = invoice_amounts[invoice.invoiceNo]
        invoice.save()
        generatepdf(invoice.id)

def generatepdf(id):
    invoice = Invoice.objects.get(id=id)
    items = InvoiceItems.objects.filter(invoice=invoice)
    items = [item for item in items]
    itemcount = len([item for item in items if item.description!='Shipping'])
    ordercount = len({item.orderNo for item in items})
    store = Store.objects.filter(storeCode=invoice.store.storeCode).first()
    taxamount = round((invoice.subTotal - invoice.discount) * invoice.taxrate * Decimal(0.01), 2)
    context = {"invoice": invoice, "items": items, "store": store, "itemcount": itemcount, "ordercount": ordercount, "taxamount": taxamount}
    template_path = 'invoiceDetails.html'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    media_root = settings.MEDIA_ROOT
    output_filename = invoice.invoiceNo + '.pdf'
    output_filepath = media_root.joinpath('invoicepdfs').joinpath(output_filename)
    result_file = open(output_filepath, "w+b")
    pisa_status = pisa.CreatePDF(
        html, dest=result_file)
    result_file.close()

    if pisa_status.err:
        print('error while generating pdf ' + output_filename)
        return

    invoice.attachment.name = 'invoicepdfs/' + output_filename
    invoice.save()

def check():
    start = date(2021, 3,15)
    end = date(2021, 6, 29)
    create_invoices(start, end)
from decimal import Decimal

from django.template.loader import get_template

from orders.models import Order
from products.models import Product
from invoices.models import Invoice, InvoiceItems
from stores.models import Store
from datetime import datetime, date, timedelta
from xhtml2pdf import pisa
from django.conf import settings
import os
from django.contrib.staticfiles import finders
import logging


# Get an instance of a logger
logger = logging.getLogger('db')


def create_invoices(startDate, endDate):
    startdatetime = datetime(startDate.year, startDate.month, startDate.day)
    enddatetime = datetime(endDate.year, endDate.month, endDate.day)

    # because sql will check on 0:00 am on end date, if shipdate was 7pm on enddate, it will not be included
    enddatetime = enddatetime + timedelta(days=1)

    # startdatetime = datetime.combine(startDate, datetime.min.time())
    # enddatetime = datetime.combine(endDate, datetime.max.time())
    shipped_orders = Order.objects.filter(shipDate__range=(startdatetime, enddatetime)).filter(orderStatus="Shipped").order_by('orderNo')
    invoice_amounts = {}
    orderNoList = []

    if len(shipped_orders) == 0:
        logger.exception(
            ' admin or system tried generated invoice for ' + str(startDate) + ' to ' + str(endDate) + ', But no shipped order during these days.')
        return 0

    for order in shipped_orders:
        try:
            invoiceno = "SFMINV-" + startDate.strftime("%m%d") + "-" + endDate.strftime("%m%d") \
                        + "-" + order.store.storeCode
            if invoiceno not in list(invoice_amounts.keys()):
                print('adding invoice for store', order.storeName)

                # invoicenote = "invoice from SFM"
                # check if the invoice already exists, if so delete the invoice and create new
                Invoice.objects.filter(invoiceNo=invoiceno).delete()
                invoice = Invoice(startDate=startDate, endDate=endDate, storeName=order.storeName, store=order.store, invoiceNo=invoiceno,
                                  status="Unpaid", notes="", subTotal=0, discount=0, taxrate=6)
                invoice.save()
                invoice_amounts[invoiceno] = 0

            # print(order.saleDate)
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
        except Exception as err:
            print('error ----', str(err))
            logger.exception('Error in invoice ' + invoiceno + ', item for order ' + order.sfmId + ', Aborting... details: ' + str(err))
            raise Exception('Error generating invoice')


    logger.info(' admin or system generated invoice for ' + str(startDate) + ' to ' + str(endDate) + ' , count: ' + str(len(invoice_amounts)))
    updateInvoices(invoice_amounts)
    return len(invoice_amounts)

def updateInvoices(invoice_amounts):
    invoices = Invoice.objects.filter(invoiceNo__in=list(invoice_amounts.keys()))
    for invoice in invoices:
        invoice.subTotal = invoice_amounts[invoice.invoiceNo]
        invoice.save()
        try:
            generatepdf(invoice.id)
        except Exception as err:
            print('Error generating pdf for invoice ' + invoice.invoiceNo, str(err))
            logger.exception('Error generating pdf for invoice ' + invoice.invoiceNo + ', details: ' + str(err))

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def generatepdf(id):
    # current_site = Site.objects.get_current()
    # print('cur site ', current_site)
    invoice = Invoice.objects.get(id=id)
    items = InvoiceItems.objects.filter(invoice=invoice)
    items = [item for item in items]
    itemcount = len([item for item in items if item.description!='Shipping'])
    ordercount = len({item.orderNo for item in items})
    store = Store.objects.filter(storeCode=invoice.store.storeCode).first()
    afterdiscount = invoice.subTotal - invoice.discount
    taxamount = round(afterdiscount * invoice.taxrate * Decimal(0.01), 2)
    logourl = settings.BACKEND_URL + "/static/logosfm2.jpg"
    context = {"invoice": invoice, "items": items, "store": store, "itemcount": itemcount, "ordercount": ordercount, "afterdiscount": afterdiscount, "taxamount": taxamount, "logourl": logourl}
    template_path = 'invoiceDetails.html'
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    media_root = settings.MEDIA_ROOT
    output_filename = invoice.invoiceNo + '.pdf'
    output_filepath = media_root.joinpath('invoicepdfs').joinpath(output_filename)
    result_file = open(output_filepath, "w+b")
    pisa_status = pisa.CreatePDF(
        html, dest=result_file, link_callback=link_callback)
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
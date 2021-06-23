from django.core.management.base import BaseCommand, CommandError
from invoices.models import Invoice
from datetime import date, timedelta, datetime
from invoices import logic

class Command(BaseCommand):
    help = 'Generate invoices for the past week (Sun-Sat)'

    # def add_arguments(self, parser):
    #     parser.add_argument('invoice_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        days = date.today().isoweekday()
        endDate = date.today() - timedelta(days=days + 1)
        startDate = date.today() - timedelta(days=days + 1) - timedelta(days=6)
        dates = str(startDate) + ' to ' + str(endDate)
        try:
            count = logic.create_invoices(startDate, endDate)
        except Exception as err:
            raise CommandError('Error creating invoices for ' + dates + '' + str(err)[0:50])
        file1 = open("invoicelogs.txt", "a")  # append mode
        file1.write(str(datetime.now()) + " created invoices for " + str(count) + dates + "\n")
        file1.close()
        self.stdout.write(self.style.SUCCESS('Successfully created %i invoices for "%s"' % (count, dates)))
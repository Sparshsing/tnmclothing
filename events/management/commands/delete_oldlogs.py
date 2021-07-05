from django.core.management.base import BaseCommand, CommandError
from invoices.models import Invoice
from datetime import date, timedelta, datetime
from events.models import StatusLog
import logging


# Get an instance of a logger
logger = logging.getLogger('db')

class Command(BaseCommand):
    help = 'deletes old db logs older than given days'

    def add_arguments(self, parser):
        parser.add_argument('n_days', nargs='+', type=int)

    def handle(self, *args, **options):
        n_days = 30
        try:
            n_days = options['n_days'][0]
        except Exception as err:
            self.stdout.write('Did not receive days argument thus using 30 days for deleting old logs')

        oldestdate = datetime.now() - timedelta(days=n_days)
        try:
            oldlogs = StatusLog.objects.filter(create_datetime__lt=oldestdate)
            oldlogs.delete()
        except Exception as err:
            logger.exception('Error in system trying to delete old logs, ' + str(err))
            raise CommandError('Error in system trying to delete old logs, ' + str(err)[0:50])

        file1 = open("invoicelogs.txt", "a")  # append mode
        file1.write(str(datetime.now()) + " deleted old logs older than days" + str(n_days) + "\n")
        file1.close()
        logger.info('deleted old logs older than days ' + str(n_days))
        self.stdout.write(self.style.SUCCESS('Successfully deleted old logs older than days ' + str(n_days)))
import logging
from django.db import models
from django.utils.translation import gettext_lazy as _

LOG_LEVELS = (
    (logging.NOTSET, _('NotSet')),
    (logging.INFO, _('Info')),
    (logging.WARNING, _('Warning')),
    (logging.DEBUG, _('Debug')),
    (logging.ERROR, _('Error')),
    (logging.FATAL, _('Fatal')),
)


class StatusLog(models.Model):
    logger_name = models.CharField(max_length=300)
    level = models.PositiveSmallIntegerField(choices=LOG_LEVELS, default=logging.ERROR, db_index=True)
    msg = models.TextField()
    trace = models.TextField(blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Created at UTC time')

    def __str__(self):
        return self.msg

    class Meta:
        ordering = ('-create_datetime',)
        verbose_name_plural = verbose_name = 'Logging'
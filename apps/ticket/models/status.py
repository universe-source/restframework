"""
工单状态表, 一般极少改动
"""
from django.db import models

from customs.models import (UpdateTable, DateTimeModel, CacheableManager)


class TicketStatus(UpdateTable, DateTimeModel):
    name = models.CharField(max_length=128, unique=True, db_index=True)
    alias = models.CharField(max_length=256)

    objects = CacheableManager()

    class Meta:
        db_table = 'ticket_status'

    def __str__(self):
        return 'Ticket Status: {} {}'.format(self.id, self.name)

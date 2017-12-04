"""
工单操作记录
"""
from django.db import models
from django.utils import timezone

from customs.models import (UpdateTable, DateTimeModel, CacheableManager)


class TicketOperate(UpdateTable, DateTimeModel):
    operate = models.CharField(max_length=32)  # 操作类型
    uid = models.IntegerField()  # 操作人
    handle_time = models.DateTimeField(default=timezone.now)  # 操作时间
    content = models.CharField(max_length=1024)  # 操作内容

    objects = CacheableManager()

    class Meta:
        db_table = 'ticket_operate'

    def __str__(self):
        return 'Ticket Operate: {}'.format(self.id)

"""
工单
"""
from django.db import models

from customs.models import (UpdateTable, DateTimeModel, CacheableManager)
from apps.config import Config
# SCORES, SCORE_5, TICKET_STATUS_CREATED, TICKET_STATUSES


class TicketTask(UpdateTable, DateTimeModel):
    title = models.CharField(max_length=512)  # 工单标题
    tid = models.IntegerField()  # 工单类型
    own = models.IntegerField()  # 工单所有者
    operator = models.IntegerField()  # 当前执行者
    status = models.CharField(max_length=20, choices=Config.TICKET_STATUSES,
                              default=Config.TICKET_STATUS_CREATED)  # 工单状态
    score = models.IntegerField(choices=Config.SCORES,
                                default=Config.SCORE_5)  # 工单评价
    content = models.CharField(max_length=1024)  # 工单描述

    objects = CacheableManager()

    class Meta:
        db_table = 'ticket_task'

    def __str__(self):
        return 'Ticket Task: {}'.format(self.id)

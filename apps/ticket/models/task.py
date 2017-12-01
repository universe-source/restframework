"""
工单
"""
from django.db import models

from customs.models import (UpdateTable, DateTimeModel, CacheableManager)
from apps.config import SCORES, SCORE_5


class TicketTask(UpdateTable, DateTimeModel):
    title = models.CharField(max_length=512)
    tid = models.IntegerField()  # 工单类型
    own = models.IntegerField()  # 工单所有者
    operator = models.IntegerField()  # 当前执行者
    status = models.IntegerField()  # 工单状态
    score = models.IntegerField(choices=SCORES, default=SCORE_5)  # 工单评价

    objects = CacheableManager()

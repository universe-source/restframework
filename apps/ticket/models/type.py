"""
工单类型, 由管理员在后台手动添加
"""
from django.db import models
#  from jsonfield import JSONField

from customs.models import (UpdateTable, DateTimeModel, CacheableManager)


class TicketType(UpdateTable, DateTimeModel):
    name = models.CharField(max_length=128, unique=True, db_index=True)  # 类型名
    alias = models.CharField(max_length=256)
    desc = models.CharField(max_length=512)  # 描述
    # TODO: 角色

    objects = CacheableManager()

    class Meta:
        db_table = 'ticket_type'

    def __str__(self):
        return 'Ticket Type: {} {}'.format(self.pk, self.name)

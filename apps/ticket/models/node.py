"""
工单审核流程节点, 上下级关系
"""
from django.db import models
from jsonfield import JSONField

from customs.models import (UpdateTable, DateTimeModel, CacheableManager)


class TicketNode(UpdateTable, DateTimeModel):
    """
        Node1:
            Child Node A
                Child Node B
                ...
            Child Node B
            ...
    """
    name = models.CharField(max_length=64, db_index=True)  # 节点名
    tid = models.IntegerField()  # 工单类型, TicketType主键
    alias = models.CharField(max_length=512)  # 描述
    # TODO: 当前节点可以操作的角色
    parent = models.CharField(max_length=64, default="")  # 父节点
    children = JSONField(default={})  # 子节点

    objects = CacheableManager()

    class Meta:
        db_table = 'ticket_node'
        unique_together = (('tid', 'name'))

    def __str__(self):
        return 'Ticket Node: {} ({}, {})'.format(self.pk, self.tid, self.name)

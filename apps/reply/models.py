"""
工单对话回复表
"""
from django.db import models
from django.utils import timezone

from customs.models import (UpdateTable, DateTimeModel, CacheableManager)
from apps.config import Config


class Reply(UpdateTable, DateTimeModel):
    fid = models.IntegerField()  # 外接类型id
    ftype = models.CharField(max_length=15, choices=Config.REPLYS,
                             default=Config.REPLY_BLOG)
    uid = models.IntegerField()  # 留言所有者
    reply_to = models.IntegerField(default=0)  # 留言reply的id值
    content = models.CharField(max_length=1024, blank=True)  # 留言
    handle_time = models.DateTimeField(default=timezone.now)  # 用户更新时间

    objects = CacheableManager()

    class Meta:
        db_table = 'reply'
        unique_together = (('fid', 'ftype'))

    def __str__(self):
        return 'Reply {} ({}{})'.format(self.id, self.fid, self.ftype)

import os
import time
import binascii
from datetime import timedelta
from django.db import models
from django.utils import timezone

from customs.models import (UpdateTable, DateTimeModel,
                            CacheableManager, UnCacheableManager)
from .person import Person


def expired_time(days=3):
    return timezone.now() + timedelta(days=days)


class AuthToken(UpdateTable, DateTimeModel):
    key = models.CharField(max_length=40, primary_key=True)
    uid = models.CharField(max_length=20, unique=True)
    expired_at = models.DateTimeField(default=expired_time)

    # 自定义管理器
    objects = CacheableManager()
    uncaches = UnCacheableManager()

    def __str__(self):
        return 'Token {} {}'.format(self.uid, self.key)

    class Meta(object):
        db_table = 'auth_token'

    @property
    def user(self):
        """在TokenAuthentication中被调用"""
        if hasattr(self, '_user'):
            return self.getattr('_user')
        self._user = Person.objects.get_or_none(id=self.uid)
        if self._user:
            # NOTE: 这里返回Person对象
            return self._user

    @property
    def expired_timestamp(self):
        return int(time.mktime(self.expired_at.timetuple()))

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):
        """
        @1 如果不存在key, 则生成新的token.
        @2 每一次保存, 都会延长token的过期时间
        """
        if not self.key:
            self.key = self.generate_key()
        self.expired_at = timezone.now() + timedelta(days=15)
        # 1 save操作默认会根据pk进行一次查找操作, 如果有缓存就跳过, 所以这里
        # 可能会多进行一次 SQL 操作
        # 2 从这里可知, 尽可能的设置primary_key
        return super(AuthToken, self).save(*args, **kwargs)

    def expired(self):
        return self.expired_at < timezone.now()

    def expire(self):
        self.expired_at = timezone.now() - timedelta(days=1)
        return super(AuthToken, self).save()

    def defer(self):
        self.expired_at = timezone.now() + timedelta(days=15)
        self.save()

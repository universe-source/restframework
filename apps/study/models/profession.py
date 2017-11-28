from django.db import models

from customs.models import (UpdateTable, DateTimeModel,
                            CacheableManager, UnCacheableManager)


class Profession(UpdateTable, DateTimeModel):
    """专业, 研究方向"""
    name = models.CharField(max_length=150)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)

    objects = CacheableManager()
    uncaches = UnCacheableManager()

    class Meta(object):
        db_table = 'profession'

    def __str__(self):
        return 'Profession {}'.format(self.id)

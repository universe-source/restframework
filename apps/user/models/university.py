from django.db import models
from django.utils import timezone

from customs.models import (UpdateTable, DateTimeModel,
                            CacheableManager, UnCacheableManager)


class University(UpdateTable, DateTimeModel):
    """大学"""
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    establish = models.DateField(default=timezone.now)
    location = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)

    objects = CacheableManager()
    uncaches = UnCacheableManager()

    class Meta(object):
        db_table = 'university'

    def __str__(self):
        return 'University {} {}'.format(self.id, self.name)

from django.db import models

from customs.models import UpdateTable, DateTimeModel


class Profession(UpdateTable, DateTimeModel):
    """专业, 研究方向"""
    name = models.CharField(max_length=150)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)

    class Meta(object):
        db_table = 'profession'

    def __str__(self):
        return 'Profession {}'.format(self.id)

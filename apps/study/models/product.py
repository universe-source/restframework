from django.db import models
from django.utils import timezone

from customs.models import UpdateTable, DateTimeModel


class Product(UpdateTable, DateTimeModel):
    """研究成果"""
    name = models.CharField(max_length=150)
    Profession_id = models.PositiveIntegerField()

    publish = models.DateTimeField(default=timezone.now)  # 发表时间
    die = models.DateTimeField(default=timezone.now)  # 消亡时间
    goal = models.IntegerField(default=0)  # 成果为人类文明所贡献的分数
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)

    class Meta(object):
        db_table = 'product'

    def __str__(self):
        return 'Product {}'.format(self.id)

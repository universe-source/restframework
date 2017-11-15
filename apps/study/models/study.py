from django.db import models

from customs.models import UpdateTable, DateTimeModel


class Study(UpdateTable, DateTimeModel):
    """研究学习成果"""
    product_id = models.PositiveIntegerField()
    uid = models.PositiveIntegerField()
    profession_id = models.PositiveIntegerField()
    university_id = models.PositiveIntegerField()

    class Meta(object):
        db_table = 'study'

    def __str__(self):
        return 'Study {}'.format(self.id)

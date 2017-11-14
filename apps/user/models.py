from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from customs.models import UpdateTable
from apps.config import GENDERS, GENDER_UNKNOWN
from apps.models import DateTimeModel


class Person(UpdateTable, DateTimeModel):
    """使用代理模式来扩展用户表, 类似一个ForeignKey, 并且设置了unique=True
        User<---->Person, 一一对应关系
    使用例子见:
        http://python.usyiyi.cn/documents/django_182/topics/db/examples/one_to_one.html
    获取queryset时, 实际 SQL 命令:
        SELECT `user_person`.`id`, `user_person`.`user_id`, `user_person`.`age`
        FROM `user_person` INNER JOIN `auth_user` 
        ON (`user_person`.`user_id` = `auth_user`.`id`) 
        ORDER BY `auth_user`.`date_joined` DESC
    """
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=50, blank=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, choices=GENDERS, default=GENDER_UNKNOWN)
    birthday = models.DateTimeField(default=timezone.now)
    country_code = models.CharField(max_length=2, default='CN')

    def __unicode__(self):
        return 'People {}'.format(self.user.id)

    class Meta(object):
        db_table = 'person'

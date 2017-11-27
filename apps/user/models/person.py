from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from customs.models import UpdateTable, DateTimeModel, CacheableManager
from apps.config import GENDERS, GENDER_UNKNOWN


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
    user = models.OneToOneField(User)  # 确保email是唯一的
    nickname = models.CharField(max_length=50, blank=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, choices=GENDERS, default=GENDER_UNKNOWN)
    birthday = models.DateTimeField(default=timezone.now)
    country_code = models.CharField(max_length=2, default='CN')
    province = models.CharField(max_length=50, blank=True)

    objects = CacheableManager()

    def __str__(self):
        return 'People {} {}'.format(self.user.id, self.nickname)

    class Meta(object):
        db_table = 'person'

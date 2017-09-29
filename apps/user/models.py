from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    """使用代理模式来扩展用户表, 类似一个ForeignKey, 并且设置了unique=True
        User<---->Person, 一一对应关系
    使用例子见:
        http://python.usyiyi.cn/documents/django_182/topics/db/examples/one_to_one.html
    """
    user = models.OneToOneField(User)
    age = models.IntegerField(default=0)

    def __unicode__(self):
        return 'People {}'.format(self.user.id)

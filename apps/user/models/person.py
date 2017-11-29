from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from customs import UpdateTable, gen_fake_email
from apps.config import GENDERS, GENDER_UNKNOWN
from ..managers import PersonManager


class Person(AbstractBaseUser, PermissionsMixin, UpdateTable):
    """ 代理模式--见分支develop_userproxy
        重写User模型;
        参考:
          http://python.usyiyi.cn/translate/django_182/topics/auth/customizing.html
          https://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True, default=gen_fake_email)
    nickname = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, choices=GENDERS, default=GENDER_UNKNOWN)
    birthday = models.DateTimeField(default=timezone.now)
    country_code = models.CharField(max_length=2, default='CN')
    province = models.CharField(max_length=50, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # 对于重写User模型, 需要一个自定义的管理器
    objects = PersonManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return 'User {} {}'.format(self.pk, self.nickname)

    class Meta(object):
        db_table = 'user'

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.nickname

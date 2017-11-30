"""
参考: http://python.usyiyi.cn/translate/django_182/topics/auth/customizing.html
功能: 对于自定义User模型, 需要一个自定义管理器
"""
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from customs import CacheableManager, gen_fake_email


class PersonManager(BaseUserManager, CacheableManager):
    """该操作用于在shell上创建用户"""
    def create_user(self, username, password, **kwargs):
        email = kwargs.get('email', gen_fake_email())
        if not username or not password or not email:
            return None

        now = timezone.now()
        user = self.model(
            email=self.normalize_email(email),  # 规范邮件, 见官网说明
            username=username,
            last_login=now, is_active=False,
            date_joined=now)
        for field in ('nickname', 'first_name', 'last_name', 'age', 'gender',
                      'birthday', 'country_code', 'province', 'is_active'):
            if field in kwargs:
                setattr(user, field, kwargs.get(field))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **kwargs):
        """其中username为USERNAME_FIELD, email为REQUIRED_FIELDS"""
        kwargs['email'] = email
        user = self.create_user(username, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

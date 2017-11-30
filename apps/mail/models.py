from django.db import models

from customs.models import (UpdateTable, DateTimeModel,
                            CacheableManager, UnCacheableManager)


class Mail(UpdateTable, DateTimeModel):
    from_email = models.EmailField()
    to_email = models.EmailField()
    subject = models.CharField(max_length=200)
    mail_type = models.CharField(max_length=15)  # 发送的邮件类型
    template = models.CharField(max_length=45)  # 使用的邮件模板
    content = models.TextField()
    error = models.CharField(max_length=150)
    transaction_id = models.CharField(max_length=32)  # 关联的发送id, EDM服务商提供
    sent = models.BooleanField(default=False)

    objects = CacheableManager()
    uncaches = UnCacheableManager()

    def __str__(self):
        return 'Mail {} {}'.format(self.uid, self.key)

    class Meta:
        db_table = 'mail'

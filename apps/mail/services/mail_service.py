"""
邮件发送记录
"""
import logging

#  import errors
from customs import BaseService, BaseSerializer
from ..models import Mail
from ..serializers import MailSerializer
from .sendcloud_service import sendcloud_service


logger = logging.getLogger('mail')


class MailService(BaseService, BaseSerializer):
    model = Mail
    serializer_class = MailSerializer
    desc = 'Mail object serializes'

    def send(self, to, subject, **kwargs):
        return sendcloud_service.send_template_simple_test(to, subject, **kwargs)

    def send_active_mail(self, to, **kwargs):
        """发送用户激活邮件, 根据模板来准备相应的数据"""
        # ready
        data = {
            'url': kwargs.get('url'),
            'username': kwargs.get('username')
        }

        # send
        result = self.send(to, kwargs.get('subject'), **data)

        # save
        from_email = sendcloud_service.from_email
        self.create(from_email=from_email,
                    to_email=to,
                    subject=result.get('subject'),
                    mail_type='trigger',
                    template=result.get('template'),
                    content=data,
                    error=result.get('error'),
                    sent=result.get('sent'))
        return result.get('sent')


mail_service = MailService()

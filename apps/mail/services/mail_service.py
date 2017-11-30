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
        succ = sendcloud_service.send_simple_test(to, subject, **kwargs)
        if succ:
            return True
        return False

    def send_active_mail(self, to, sign, **kwargs):
        """发送用户激活邮件"""
        # ready
        subject = kwargs.get('subject', '用户激活邮件')
        content = '激活: http://127.0.0.1:8082/users/validate/?sign={}'.format(sign)
        data = {
            'content': content
        }

        # send
        succ = self.send(to, subject, **data)

        # save
        sent = True if succ else False
        from_email = sendcloud_service.from_email
        mail_type = 'test'
        self.create(from_email=from_email,
                    to_email=to,
                    subject=subject,
                    mail_type=mail_type,
                    template='test',
                    content=content,
                    sent=sent)
        return sent


mail_service = MailService()

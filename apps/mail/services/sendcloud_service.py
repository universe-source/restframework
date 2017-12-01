"""
sendcloud EDM mail service
Reference: http://www.sendcloud.net/doc/guide/base/
1 模板发送:
    -> 根据不同的功能选择"触发邮件"/"批量邮件"的APP_USER;
    -> 根据模板准备不同的数据;
    -> 调用发送 API;
    -> 存储发送的信息到本地 DB 中.
"""
import json
import requests
from ..config import SENDCLOUD_ACTIVE_EMAIL


class SendCloudService(object):
    def __init__(self, url, key, user, **kwargs):
        self.url = url
        self.key = key
        self.user = user
        self.from_email = kwargs.get('from_mail', 'service@sendcloud.im')
        self.from_name = kwargs.get('from_name', 'Default Name')
        self.template = kwargs.get('template', 'test_template_active')

    def send_template_simple_test(self, to, subject, **kwargs):
        xsmtpapi = {
            'to': [to],
            'sub': {
                '%name%': [kwargs.get('username')],
                '%url%': [kwargs.get('url')],
            }
        }
        template = 'test_template_active'
        params = {
            'apiUser': self.user,
            'apiKey': self.key,
            'templateInvokeName': template,
            'from': self.from_email,
            'fromName': self.from_name,
            'xsmtpapi': json.dumps(xsmtpapi),
        }
        if subject:
            params['subject'] = subject

        result = {
            'template': template,
            'sent': False,
            'error': 'Unreach network',
            'subject': subject if subject else 'Default Subject of Template'
        }
        r = requests.post(self.url, files={}, data=params)
        if r and r.status_code == 200:
            data = json.loads(r.text)
            if data.get('result') is True:
                result['sent'] = True
                result['error'] = ''
            else:
                result['error'] = '{}: {}'.format(data.get('statusCode'),
                                                  data.get('message'))
        return result


# 根据模板发送邮件
sendcloud_service = SendCloudService(
    SENDCLOUD_ACTIVE_EMAIL.get('url'),
    SENDCLOUD_ACTIVE_EMAIL.get('key'),
    SENDCLOUD_ACTIVE_EMAIL.get('user'),
    **{
        'from': SENDCLOUD_ACTIVE_EMAIL.get('from'),
        'from_name': SENDCLOUD_ACTIVE_EMAIL.get('from_name'),
        'template': SENDCLOUD_ACTIVE_EMAIL.get('template'),
    })

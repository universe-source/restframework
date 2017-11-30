"""
sendcloud EDM mail service
"""
import json
import requests
from ..config import (SENDCLOUD_KEY, SENDCLOUD_USER, SENDCLOUD_URL,
                      SENDCLOUD_TEMPLATE_URL)


class SendCloudService(object):
    def __init__(self, url, template_url, key, user):
        self.url = url
        self.template_url = template_url
        self.key = key
        self.user = user
        self.from_email = 'service@sendcloud.im'

    def send_simple_test(self, to, subject, **kwargs):
        params = {
            'apiUser': self.user,
            'apiKey': self.key,
            'from': self.from_email,
            'fromName': '测试邮件',
            'to': to,
            'subject': subject,
            'html': kwargs.get('content')
        }
        r = requests.post(self.url, files={}, data=params)
        if r and r.status_code == 200:
            print('Value:', r.text)
            return True
        return False

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
            'fromName': '激活邮件',
            #  'subject': subject,
            'xsmtpapi': json.dumps(xsmtpapi),
        }

        result = {
            'tempate': template,
            'sent': False,
            'error': 'Unreach network',
        }
        r = requests.post(self.template_url, files={}, data=params)
        if r and r.status_code == 200:
            data = json.loads(r.text)
            if data.get('result') is True:
                result['sent'] = True
                result['error'] = ''
            result['error'] = '{}: {}'.format(data.get('statusCode'),
                                              data.get('message'))
        return result


sendcloud_service = SendCloudService(SENDCLOUD_URL, SENDCLOUD_TEMPLATE_URL,
                                     SENDCLOUD_KEY, SENDCLOUD_USER)

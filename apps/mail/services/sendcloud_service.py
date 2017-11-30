"""
sendcloud EDM mail service
"""
import requests
from ..config import SENDCLOUD_KEY, SENDCLOUD_USER, SENDCLOUD_URL


class SendCloudService(object):
    def __init__(self, url, key, user):
        self.url = url
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


sendcloud_service = SendCloudService(SENDCLOUD_URL, SENDCLOUD_KEY, SENDCLOUD_USER)

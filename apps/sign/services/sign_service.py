"""
使用itsdangerous生成时间戳签名: http://itsdangerous.readthedocs.io/en/latest/
"""
import logging
from urllib.parse import parse_qs, urlencode
import itsdangerous
from itsdangerous import URLSafeTimedSerializer as utsr
from django.conf import settings


logger = logging.getLogger('sign')


class UtsrTimeSign(object):
    EXPIRED = 12 * 3600

    def __init__(self, security_key, salt="validateToken"):
        self.security_key = security_key
        self.salt = salt  # 命名空间, 并非安全中的盐值

    def parse_qs_value(self, value):
        """value格式:  id=x&username=x"""
        values = parse_qs(value)
        if 'id' in values and 'username' in values:
            return {
                'id': int(values.get('id')[0]),
                'username': values.get('username')[0],
            }
        return None

    def encode_qs_value(self, **values):
        return urlencode(values)

    def generate_validate_sign(self, value):
        """其中value一般为多个字段连接在一起的字符串"""
        serializer = utsr(self.security_key)
        return serializer.dumps(value, self.salt)

    def confirm_validate_sign(self, sign, expiration=EXPIRED):
        serializer = utsr(self.security_key)
        try:
            value = serializer.loads(sign, salt=self.salt, max_age=expiration)
        except itsdangerous.SignatureExpired:
            logger.info('Sign already expired: {}.'.format(sign))
            return False, None
        except itsdangerous.BadData:
            logger.error('Validate sign failed: {}.'.format(sign))
            return False, None
        else:
            return True, value


utsrtimesign_service = UtsrTimeSign(settings.SECRET_KEY)

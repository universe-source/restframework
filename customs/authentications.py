"""
授权认证
"""
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AnonymousUser

import errors
from errors.exceptions import XAuthenticationFailed
from apps.user.models import AuthToken


class XTokenAuthentication(TokenAuthentication):
    model = AuthToken

    def __init__(self, *args, **kwargs):
        super(XTokenAuthentication, self).__init__(*args, **kwargs)
        self.user = AnonymousUser()
        self.token = None
        self.key = None

    def authenticate_header(self, request):
        return 'Token'

    def get_model(self):
        return self.model

    def authenticate_credentials(self, key):
        """rewrite: 返回(user, token)"""
        if key == self.key:
            return (self.user, self.token)
        token = self.model.objects.get_or_none(key=key)
        if token and not token.expired():
            self.user = token.user
            self.token = token
            self.key = key
            return (self.user, self.token)
        elif token and token.expired:
            raise XAuthenticationFailed(code=errors.CODE_EXPIRED_TOKEN)
        else:
            raise XAuthenticationFailed(code=errors.CODE_BAD_TOKEN)

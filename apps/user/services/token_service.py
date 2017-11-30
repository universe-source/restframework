from customs import BaseService, BaseSerializer
from ..models import AuthToken
from ..serializers import TokenSerializer


class TokenService(BaseService, BaseSerializer):
    model = AuthToken
    serializer_class = TokenSerializer
    desc = 'Token object serialize'

    def login(self, person):
        """登录并刷新token, 如果未过期则延长过期时间"""
        token = self.get_or_none(uid=person.id)
        if token.expired():
            token.delete()
            token = self.get_or_create(uid=person.id)
        else:
            token.save()
        return token

    def expire(self, person):
        token = self.get_or_none(uid=person.id)
        if token:
            token.expire()

    def defer(self, person):
        token = self.get_or_none(uid=person.id)
        if token:
            token.defer()
            return True
        return False


token_service = TokenService()

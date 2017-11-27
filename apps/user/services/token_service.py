from customs import BaseService
from ..models import AuthToken
from ..serializers import TokenSerializer


class TokenService(BaseService):
    model = AuthToken
    serializer_class = TokenSerializer
    desc = 'Token object serialize'

    def serialize(self, obj, context=None):
        """序列化某一个单一对象"""
        context = {'desc': self.desc} if not context else context
        return self.serializer_class(obj, context=context).data

    def serializes(self, objs):
        """序列化某一个对象列表"""
        return [self.serialize(obj) for obj in objs]

    def login(self, person):
        """登录并刷新token, 如果未过期则延长过期时间"""
        token = self.get_or_none(uid=person.id)
        if token.expired():
            token.delete()
            token = self.get_or_create(uid=person.id)
        else:
            token.save()
        return token

    def defer(self, person):
        token = self.get_or_none(uid=person.id)
        if token:
            token.defer()
            return True
        return False


token_service = TokenService()

"""
person基本操作
"""
from django.db import transaction
from django.contrib.auth import authenticate as _authenticate

from customs import BaseService
from .token_service import token_service
from ..models import Person
from ..serializers import PersonSerializer


class PersonService(BaseService):
    model = Person
    serializer_class = PersonSerializer
    desc = 'Person object serializes'

    def serialize(self, obj, context=None):
        """序列化某一个单一对象"""
        context = {'desc': self.desc} if not context else context
        return self.serializer_class(obj, context=context).data

    def serializes(self, objs):
        """序列化某一个对象列表"""
        return [self.serialize(obj) for obj in objs]

    @transaction.atomic
    def login(self, username, password):
        """登录, 验证, 并自动延长token的过期时间"""
        if '@' in username:
            person = self.get_or_none(user__email=username)
            if person:
                username = person.user.username
            else:
                username = None
        if username:
            user = _authenticate(username=username, password=password)
            if user:
                person = self.get_or_none(user=user)
                if person:
                    token = token_service.login(person)
                    person.token = token
                    return person
        return None

    def logout(self, person):
        pass

    def auth(self, key):
        token = token_service.get_or_none(key=key)
        if token and not token.expired():
            person = self.get_or_none(id=token.uid)
            person.token = token
            return person
        return None

    def defer(self, person):
        return token_service.defer(person)


person_service = PersonService()

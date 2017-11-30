"""
person基本操作
"""
import logging
import base64
from django.db import transaction
from django.contrib.auth import authenticate as _authenticate

import errors
from customs import BaseService, BaseSerializer
from apps.sign.services import utsrtimesign_service
from apps.mail.services import mail_service
from .token_service import token_service
from ..models import Person
from ..serializers import PersonSerializer


logger = logging.getLogger('user')


class PersonService(BaseService, BaseSerializer):
    model = Person
    serializer_class = PersonSerializer
    desc = 'Person object serializes'

    @transaction.atomic
    def login(self, username, password):
        """登录, 验证, 并自动延长token的过期时间"""
        if '@' in username:
            person = self.get_or_none(email=username)
            if person:
                username = person.username
            else:
                username = None
        if username:
            person = _authenticate(username=username, password=password)
            if person:
                token = token_service.login(person)
                person.token = token
                return person
        return None

    def logout(self, person):
        return token_service.expire(person)

    def auth(self, key):
        token = token_service.get_or_none(key=key)
        if token and not token.expired():
            person = self.get_or_none(id=token.uid)
            person.token = token
            return person
        return None

    def _generate_sign(self, person):
        username = base64.b64encode(person.username.encode('utf8'))
        kwargs = {
            'username': username,
            'id': person.id
        }
        value = utsrtimesign_service.encode_qs_value(**kwargs)
        sign = utsrtimesign_service.generate_validate_sign(value)
        return sign

    @transaction.atomic
    def register(self, username, password, **kwargs):
        """注册用户"""
        email = kwargs.get('email')
        person = self.get_or_none(email=email)
        if not person:
            kwargs['is_active'] = False
            person = self.model.objects.create_user(username, password, **kwargs)
            if person:
                # TODO: send email to user
                sign = self._generate_sign(person)
                person.sign = sign
                mail_service.send_active_mail('unusebamboo@163.com', sign)
                return True, person
            logger.error('Create user failed, check: username, password, email')
            return False, errors.CODE_CREATE_USER_FAILED
        return False, errors.CODE_EXISTED_EMAIL

    def validate(self, sign):
        """value格式: id=x&token=x"""
        succ, value = utsrtimesign_service.confirm_validate_sign(sign)
        if succ:
            values = utsrtimesign_service.parse_qs_value(value)
            if values:
                username = base64.b64decode(values.get('username')).decode('utf8')
                person = self.get_or_none(pk=values.get('id'))
                if person and person.username == username:
                    person.is_active = True
                    person.save()
                    return True, person
                return False, errors.CODE_BAD_TOKEN
            logger.info('Bad sign source data:{}'.format(value))
            return False, errors.CODE_BAD_SIGN

        return False, errors.CODE_BAD_SIGN


person_service = PersonService()

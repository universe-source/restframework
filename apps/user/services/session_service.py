"""
使用 DB 作为session存储构件
"""
from django.contrib.sessions.models import Session
from customs import BaseService, BaseSerializer


class SessionService(BaseService, BaseSerializer):
    model = Session


session_service = SessionService()

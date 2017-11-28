"""
使用 DB 作为session存储构件
"""
from django.contrib.sessions.models import Session
from customs import BaseService


class SessionService(BaseService):
    model = Session


session_service = SessionService()

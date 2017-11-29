# -*- coding:utf-8 -*-
from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

from apps.config import SESSION_KEY
from apps.user.services import person_service


class AllowPostPermission(permissions.BasePermission):
    """
    Allow Post Method
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return False


def is_authenticated(request):
    """Token authenticated and session authenticated"""
    if request.user and not isinstance(request.user, AnonymousUser):
        return True
    print('===================session==================')
    sessionid = request.session.get(SESSION_KEY)
    person = person_service.get_or_none(id=sessionid)
    if person:
        request.user = person
        return True
    return False


def check_authorized(request, pk=None):
    """
    功能:
        1 验证用户;
        2 如果存在pk, 判断是否为本人
    """
    # NOTE: 对于User Proxy, 有一些特殊处理, 以后不建议使用 User Proxy, 过于麻烦
    #       在该项目中仅仅作为一个实验
    if is_authenticated(request):
        if request.user.user and request.user.user.is_authenticated:
            if pk:
                pk = int(pk)
                if request.user.pk != pk and not request.user.user.is_superuser:
                    return False
            return True
    return False


def check_admin_authorized(request):
    if is_authenticated(request):
        if request.user.user:
            if request.user.user.is_authenticated and request.user.user.is_superuser:
                return True
    return False

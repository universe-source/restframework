# -*- coding:utf-8 -*-
from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser


class AllowPostPermission(permissions.BasePermission):
    """
    Allow Post Method
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return False


def check_authorized(request, pk=None):
    """验证用户; 如果存在pk, 判断是否为本人"""
    # NOTE: 对于User Proxy, 有一些特殊处理
    if (not request.user or isinstance(request.user, AnonymousUser) or
            not request.user.user):
        print('xxxxxxxxxxxxxxxxxxx1')
        return False
    if not request.user.user.is_authenticated:
        print('xxxxxxxxxxxxxxxxxxx2')
        return False
    if pk and (request.user.pk != pk and not request.user.user.is_superuser):
        print('xxxxxxxxxxxxxxxxxxx3')
        return False
    return True


def check_admin_authorized(request):
    if (not request.user or isinstance(request.user, AnonymousUser) or
            not request.user.user):
        return False
    if not request.user.user.is_authenticated or not request.user.user.is_superuser:
        return False
    return True

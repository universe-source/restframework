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
    # NOTE: 对于User Proxy, 有一些特殊处理
    if (not request.user or not request.user.user or
            isinstance(request.user.user, AnonymousUser)):
        return False
    if not request.user.user.is_authenticated:
        return False
    if pk and (request.user.pk != pk and not request.user.user.is_admin):
        return False
    return True


def check_admin_authorized(request):
    if (not request.user or not request.user.user or
            isinstance(request.user.user, AnonymousUser)):
        return False
    if not request.user.user.is_authenticated or not request.user.user.is_admin:
        return False
    return True

# -*- coding:utf-8 -*-
import functools

import errors
from errors.exceptions import XAuthenticationFailed, XValidationError
from customs.permissions import check_authorized, check_admin_authorized

from .services import person_service


def login_required(func):
    @functools.wraps(func)
    def func_wrapper(self, request, *args, **kwargs):
        if not check_authorized(request):
            raise XAuthenticationFailed(code=errors.CODE_UNAUTHORIZED)
        return func(self, request, *args, **kwargs)
    return func_wrapper


def admin_required(func):
    @functools.wraps(func)
    def func_wrapper(self, request, *args, **kwargs):
        if not check_admin_authorized(request):
            raise XAuthenticationFailed(code=errors.CODE_UNAUTHORIZED)
        return func(self, request, *args, **kwargs)
    return func_wrapper


def is_user_self(func):
    @functools.wraps(func)
    def user_wrapper(self, request, pk, *args, **kwargs):
        if not check_authorized(request, pk):
            raise XAuthenticationFailed(code=errors.CODE_UNAUTHORIZED)
        person = person_service.get_or_none(id=pk)
        if not person:
            raise XValidationError(code=errors.CODE_UNEXIST_USER)
        request.user = person
        return func(self, request, pk, *args, **kwargs)

    return user_wrapper


def permission_required(target='user_self', action=None):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if not check_authorized(request):
                raise XAuthenticationFailed(code=errors.CODE_UNAUTHORIZED)
            person = person_service.get_or_none(id=kwargs.get('id'))
            if not person:
                raise XValidationError(code=errors.CODE_UNEXIST_USER)
            request.user = person
            return func(self, request, *args, **kwargs)
        return wrapper
    return actual_decorator

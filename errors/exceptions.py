# -*- coding:utf-8 -*-

from json import JSONEncoder
import logging

from rest_framework import status as _status
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _

import errors


logger = logging.getLogger('common')


class APIError(exceptions.APIException):

    """
    Modified rest_framework's APIException to add more detail of the errors.
    """
    status_code = _status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _(errors.CODE_DEFAULT_BUSY)

    def __init__(self, code='', status=_status.HTTP_200_OK):
        self.detail = {
            'request': 'fail',
        }
        if code != '':
            self.detail['errors'] = {
                'message': errors.messages.get(code),
                'code': code
            }
        APIError.status_code = status
        logger.error(JSONEncoder().encode(self.detail))

    def __str__(self):
        return JSONEncoder().encode(self.detail)


class XAuthenticationFailed(APIError):
    def __init__(self, code=''):
        super(XAuthenticationFailed, self).__init__(
            code, status=_status.HTTP_401_UNAUTHORIZED)


class XPermissionDenied(APIError):
    def __init__(self, code=0):
        super(XPermissionDenied, self).__init__(code, status=_status.HTTP_403_FORBIDDEN)


class XAPI404Error(APIError):
    def __init__(self, code=0):
        super(XAPI404Error, self).__init__(code, status=_status.HTTP_404_NOT_FOUND)


class XValidationError(APIError):
    def __init__(self, code=0):
        super(XValidationError, self).__init__(
            code, status=_status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
from django.http import JsonResponse

import errors


class SimpleResponse(Response):
    """
        1) code和status决定该 API 是否成功调用.
        2) data 是返回的数据,与是否成功调用无光.
        3) message用于错误描述信息, 一般和 HTTP 4XX 码配合使用.
    """

    def __init__(self, data=None, message='', code=None, **kwargs):
        status = kwargs.get('status', 200)
        response = {
            'request': 'success' if (status / 100 == 2 and not code) else 'fail',
        }
        if data is not None:
            response['data'] = data
        if code:
            response['errors'] = {
                'message': errors.messages.get(code, errors.CODE_DEFAULT_BUSY),
                'code': code
            }
        if message:
            response.setdefault('errors', {})
            response['errors']['message'] = message
        super(SimpleResponse, self).__init__(response, **kwargs)


class SimpleJsonResponse(JsonResponse):
    def __init__(self, data=None, code=None, message=None, **kwargs):
        status = kwargs.get('status', 200)
        response = {
            'request': 'success' if (status / 100 == 2 and not code) else 'fail',
        }
        if data is not None:
            response['data'] = data
        if code:
            response['errors'] = {
                'message': errors.messages.get(code, errors.CODE_DEFAULT_BUSY),
                'code': code
            }
        if message:
            response.setdefault('errors', {})
            response['errors']['message'] = message
        super(SimpleJsonResponse, self).__init__(data=response, **kwargs)

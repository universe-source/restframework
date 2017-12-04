"""
Ticket Handle Api
"""
from rest_condition import Or
from rest_framework import viewsets, permissions
from rest_framework.authentication import BasicAuthentication
#  from rest_framework.decorators import detail_route

import errors
from customs.authentications import XTokenAuthentication
from customs.permissions import AllowPostPermission
from customs import SimpleResponse, check_params, filter_params
from apps.user.permissions import is_user_self
from ..models import TicketTask
from ..serializers import TicketTaskSerializer
from ..services import ticket_task_service


class TicketTaskViewSet(viewsets.ViewSet):
    queryset = TicketTask.objects.all().order_by('-created')
    serializer_class = TicketTaskSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    authentication_classes = (BasicAuthentication, XTokenAuthentication)
    permission_classes = [
        Or(permissions.IsAuthenticatedOrReadOnly, AllowPostPermission, )]

    def create(self, request):
        """
        desc: create a ticket
        parameters:
        - name: body
            paramType: body
            location: body
            required: True
        Example Request:
            {
            "title": "xxx",
            "type": "ticket type",
            "content": "ticket task content"
            }
        """
        succ, params = check_params(request.data, ('title', 'type', 'content'))
        if succ:
            succ, task = ticket_task_service.create(**params)
            if succ:
                data = ticket_task_service.serialize(task)
                return SimpleResponse(data=data)
            return SimpleResponse(code=errors.CODE_CREATE_TICKET_TASK_FAILED)
        return SimpleResponse(code=errors.CODE_BAD_ARGUMENT)

    @is_user_self
    def update(self, request, pk):
        """
        desc: close a ticket task
        parameters:
        - name: body
            paramType: body
            location: body
            required: True
        Example Request:
        {
            "action": "close/confirm"
        }
        or
        {
            "action": "score",
            "score": 1/2/3/4/5
        }
        """
        params = filter_params(request.data, ('action', 'score'))
        task = ticket_task_service.get_or_none(pk=pk)
        if task:
            action = params.pop('action')
            succ = False
            task = errors.CODE_BAD_ARGUMENT
            if action == 'close':
                succ, task = ticket_task_service.close(task)
            elif action == 'confirm':
                succ, task = ticket_task_service.confirm(task)
            elif action == 'score':
                succ, task = ticket_task_service.confirm(task, **params)

            if succ:
                data = ticket_task_service.serialize(task)
                return SimpleResponse(data=data)
            return SimpleResponse(code=task)

        return SimpleResponse(code=errors.CODE_UNEXIST_TICKET_TASK)

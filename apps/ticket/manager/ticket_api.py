"""
Ticket Handle Api of Manager
"""
from rest_condition import Or
from rest_framework import viewsets, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route

import errors
from customs.authentications import XTokenAuthentication
from customs.permissions import AllowPostPermission
from customs import SimpleResponse, check_params, filter_params
from apps.user.permissions import admin_required
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

    @admin_required
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

    @list_route(methods=['post'], url_path='type')
    @admin_required
    def add_ticket_type(self, request):
        """
        desc: Add a new ticket type
        parameters:
        - name: body
            paramType: body
            location: body
            required: True
        Example Request:
        {
            "name": "type",
            "alias": "alias name",
            "audit": {
            },
            "desc": "This is description of current ticket type."
        }
        """
        pass

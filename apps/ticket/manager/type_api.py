"""
Ticket Type Handle Api of Manager
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
from ..models import TicketType
from ..serializers import TicketTypeSerializer
from ..services import ticket_type_service, ticket_node_service


class TicketTypeViewSet(viewsets.ViewSet):
    queryset = TicketType.objects.all().order_by('-created')
    serializer_class = TicketTypeSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    authentication_classes = (BasicAuthentication, XTokenAuthentication)
    permission_classes = [
        Or(permissions.IsAuthenticatedOrReadOnly, AllowPostPermission, )]

    @admin_required
    def create(self, request):
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
            "desc": "This is descript of current ticket type."
        }
        """
        succ, params = check_params(request.data, ('name', 'alias', 'desc'))
        if succ:
            ticket_type = ticket_type_service.create(**params)
            if ticket_type:
                data = ticket_type_service.serialize(ticket_type)
                return SimpleResponse(data=data)
            return SimpleResponse(code=errors.CODE_CREATE_TICKET_TYPE_FAILED)
        return SimpleResponse(code=errors.CODE_BAD_ARGUMENT)

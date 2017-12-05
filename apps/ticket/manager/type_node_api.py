"""
Ticket Type Node Handle API of Manager
"""
from rest_condition import Or
from rest_framework import viewsets, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route, detail_route

import errors
from customs.authentications import XTokenAuthentication
from customs.permissions import AllowPostPermission
from customs import SimpleResponse, check_params, filter_params
from apps.user.permissions import admin_required
from ..models import TicketNode
from ..serializers import TicketNodeSerializer
from ..services import ticket_type_service, ticket_node_service


class TicketTypeViewSet(viewsets.ViewSet):
    queryset = TicketNode.objects.all().order_by('-created')
    serializer_class = TicketNodeSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    authentication_classes = (BasicAuthentication, XTokenAuthentication)
    permission_classes = [
        Or(permissions.IsAuthenticatedOrReadOnly, AllowPostPermission, )]

    @admin_required
    def create(self, request, tid):
        """
        desc: Create a new leaf node
        parameters:
        - name: parent
            paramType: query
            location: query
            required: True
        """
        succ, params = check_params(request.query_params, ('parent', ))
        if succ:
            ticket_type = ticket_type_service.get_or_none(pk=tid)
            if ticket_type:
                print(params)
            return SimpleResponse(code=errors.CODE_UNEXIST_TICKET_TYPE)
        return SimpleResponse(code=errors.CODE_BAD_ARGUMENT)

    @admin_required
    def update(self, request, tid, nid):
        ticket_type = ticket_type_service.get_or_none(pk=tid)
        if not ticket_type:
            pass
        return SimpleResponse(code=errors.CODE_ALREADY_EXISTED_TICKET_TYPE)

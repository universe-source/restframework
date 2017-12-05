"""
Ticket Type Handle Api of Manager
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
            # 树结构, 图结构太过于复杂
            "nodes": {
                "node1": {
                    "alias": "I am node1",
                    "parent": "",
                    "children": ["node2", "node5"],
                },
                "node2": {
                    "parent": "node1",
                    ...
                }
            }
        }
        """
        succ, params = check_params(request.data, ('name', 'alias', 'desc'))
        if succ:
            name = params.pop('name')
            nodes = request.data.get('nodes')
            succ, data = ticket_type_service.create_with_nodes(name, nodes, **params)
            if succ:
                return SimpleResponse(data=data)
            return SimpleResponse(code=data)
        return SimpleResponse(code=errors.CODE_BAD_ARGUMENT)

    @admin_required
    def update(self, request, pk):
        """
        desc: update a ticket type and all nodes
        parameters:
        - name: body
            paramType: body
            location: body
            required: True
        Example Request:
        {
            "alias": "alias name",
            "desc": "This is descript of current ticket type."
            # 树结构, 图结构太过于复杂
            "nodes": {
                "node1": {
                    "alias": "I am node1",
                    "parent": "",
                    "children": ["node2", "node5"],
                },
                "node2": {
                    "parent": "node1",
                    ...
                }
            }
        }
        """
        params = filter_params(request.data, ('alias', 'desc'))
        succ, data = ticket_type_service.update_with_nodes(
            pk, request.data.get('nodes'), **params)
        if succ:
            return SimpleResponse(data=data)
        return SimpleResponse(code=data)

    @admin_required
    def destroy(self, request, pk):
        ticket_type = ticket_type_service.get_or_none(pk=pk)
        if ticket_type:
            ticket_type_service.destory(ticket_type)
            return SimpleResponse(code=errors.CODE_SUCCESSFUL)
        return SimpleResponse(code=errors.CODE_UNEXIST_TICKET_TYPE)

    @detail_route(methods=['post', 'delete', 'put'])
    @admin_required
    def tree(self, request, pk):
        """
        desc: add/move/delete a subtree node
        parameters:
        - name: body
            paramType: body
            location: body
            required: True
        Example Request:
        # add
        {
            "parent": "parent node",
            "subroot": "subtree root node",
            "nodes": {
                "node1": {...},
                "node2": {...}
            }
        }
        # move
        {
            "src": "src parent node",
            "dst": "dst parent node",
            "subroot": "subtree root node"
        }
        """
        ticket_type = ticket_type_service.get_or_none(pk=pk)
        if not ticket_type:
            return SimpleResponse(code=errors.CODE_UNEXIST_TICKET_TYPE)

        if request.method == 'POST':
            succ, params = check_params(request.data, ('parent', 'nodes', 'subroot'))
            if succ:
                parent = ticket_node_service.get_or_none(name=params.pop('parent'))
                if parent:
                    succ, root = ticket_node_service.add_subtree(
                        ticket_type.id, parent, params.pop('subroot'), **params)
                    if succ:
                        data = ticket_node_service.serialize_tree(ticket_type.id, root)
                        return SimpleResponse(data=data)
                    return SimpleResponse(code=root)
                return SimpleResponse(code=errors.CODE_UNEXIST_TICKET_NODE)
            return SimpleResponse(code=errors.CODE_BAD_ARGUMENT)
        elif request.method == 'PUT':
            succ, params = check_params(request.data, ('src', 'dst', 'subroot'))
            if succ:
                succ, root = ticket_node_service.move_subtree(
                    ticket_type.id, params.get('src'), params.get('dst'),
                    params.get('subroot'))
                if succ:
                    data = ticket_node_service.serialize_tree(ticket_type.id, root)
                    return SimpleResponse(data=data)
                return SimpleResponse(code=root)
            return SimpleResponse(code=errors.CODE_BAD_ARGUMENT)
        elif request.method == 'DELETE':
            succ, params = check_params(request.data, ('subroot'))
            if succ:
                succ, root = ticket_node_service.delete_subtree(params.get('subroot'))
                if succ:
                    data = ticket_node_service.serialize_tree(ticket_type.id, root)
                    return SimpleResponse(data=data)
                return SimpleResponse(code=root)
            return SimpleResponse(code=errors.CODE_BAD_ARGUMENT)

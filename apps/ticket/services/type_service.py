"""
Type Service
"""
import logging
from django.db import transaction

import errors
from customs import BaseService, BaseSerializer
from ..models import TicketType
from ..serializers import TicketTypeSerializer
from .node_service import ticket_node_service


logger = logging.getLogger('ticket')


class TicketTypeService(BaseService, BaseSerializer):
    model = TicketType
    serializer_class = TicketTypeSerializer
    desc = 'Ticket Type object serialize'

    @transaction.atomic
    def destory(self, ticket_type):
        ticket_type.delete()
        ticket_node_service.filter(tid=ticket_type.id).delete()
        return True

    @transaction.atomic
    def create_with_nodes(self, name, nodes=None, **params):
        ticket_type = ticket_type_service.get_or_none(name=name)
        if not ticket_type:
            ticket_type = ticket_type_service.create(
                name=name, alias=params.get('alias', ''), desc=params.get('desc', ''))
            if ticket_type:
                data = ticket_type_service.serialize(ticket_type)
                if nodes:
                    ticket_nodes = ticket_node_service.update_or_create_tree(
                        ticket_type, **nodes)
                    data['node'] = ticket_node_service.serializes(ticket_nodes)
                return True, data
            return False, errors.CODE_CREATE_TICKET_TYPE_FAILED
        return False, errors.CODE_ALREADY_EXISTED_TICKET_TYPE

    @transaction.atomic
    def update_with_nodes(self, tid, nodes=None, **params):
        ticket_type = ticket_type_service.get_or_none(pk=tid)
        if ticket_type:
            alias = params.get('alias')
            desc = params.get('desc')
            if alias:
                ticket_type.alias = alias
            if desc:
                ticket_type.desc = alias
            if alias and desc:
                ticket_type.save()

            data = ticket_type_service.serialize(ticket_type)
            if nodes:
                ticket_nodes = ticket_node_service.update_or_create_tree(
                    ticket_type, **nodes)
                data['node'] = ticket_node_service.serializes(ticket_nodes)
            return True, data
        return False, errors.CODE_UNEXIST_TICKET_TYPE


ticket_type_service = TicketTypeService()

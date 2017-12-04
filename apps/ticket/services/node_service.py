"""
Node Service
"""
import logging

import errors
from customs import BaseService, BaseSerializer
from apps.config import Config
from ..models import TicketNode
from ..serializers import TicketNodeSerializer


logger = logging.getLogger('ticket')


class TicketNodeService(BaseService, BaseSerializer):
    model = TicketNode
    serializer_class = TicketNodeSerializer
    desc = 'Ticket Node object serialize'


ticket_node_service = TicketNodeService()

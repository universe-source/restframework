"""
Type Service
"""
import logging

from customs import BaseService, BaseSerializer
from ..models import TicketType
from ..serializers import TicketTypeSerializer


logger = logging.getLogger('ticket')


class TicketTypeService(BaseService, BaseSerializer):
    model = TicketType
    serializer_class = TicketTypeSerializer
    desc = 'Ticket Type object serialize'


ticket_type_service = TicketTypeService()

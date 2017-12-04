"""
Operate Service
"""
import logging

from customs import BaseService, BaseSerializer
from ..models import TicketOperate
from ..serializers import TicketOperateSerializer


logger = logging.getLogger('ticket')


class TicketOperateService(BaseService, BaseSerializer):
    model = TicketOperate
    serializer_class = TicketOperateSerializer
    desc = 'Ticket Operate object serialize'


ticket_operate_service = TicketOperateService()

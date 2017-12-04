"""
Task Service
"""
import logging

import errors
from customs import BaseService, BaseSerializer
from apps.config import Config
from ..models import TicketTask
from ..serializers import TicketTaskSerializer


logger = logging.getLogger('ticket')


class TicketTaskService(BaseService, BaseSerializer):
    model = TicketTask
    serializer_class = TicketTaskSerializer
    desc = 'Ticket Task object serialize'

    def close(self, task):
        if task.status == Config.TICKET_STATUS_CREATED:
            task.status = Config.TICKET_STATUS_CLOSED
            task.save()
            return True, task
        return False, errors.CODE_NOTALLOW_CHANGE_TICKET_STATUS

    def confirm(self, task):
        if task.status == Config.TICKET_STATUS_HANDLED:
            task.status = Config.TICKET_STATUS_CONFIRMED
            task.save()
            return True, task
        return False, errors.CODE_NOTALLOW_CHANGE_TICKET_STATUS

    def score(self, task, **kwargs):
        if task.status == Config.TICKET_STATUS_CONFIRMED:
            score = kwargs.get('score')
            if score >= Config.SCORE_BEGIN and score <= Config.SCORE_END:
                task.status = Config.TICKET_STATUS_SCORED
                task.score = score
                task.save()
                return True, task
            return False, errors.CODE_NOTALLOW_SCORE_TICKET_TASK
        return False, errors.CODE_NOTALLOW_CHANGE_TICKET_STATUS


ticket_task_service = TicketTaskService()

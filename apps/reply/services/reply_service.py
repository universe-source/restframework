"""
Reply Service
"""
import logging
from django.db.models import Q

from customs import BaseService, BaseSerializer
from ..models import Reply
from ..serializers import ReplySerializer


logger = logging.getLogger('reply')


class ReplyService(BaseService, BaseSerializer):
    model = Reply
    serializer_class = ReplySerializer
    desc = 'Reply object serializes'

    def replies(self, fid, ftype, **kwargs):
        """根据外接类型id, ftype等等条件, 获取所有的回复, 聊天信息"""
        rs = self.filter(fid=fid, ftype=ftype, **kwargs)
        if rs:
            return rs
        logging.info('Not found replies for: {} {} {}'.format(fid, ftype, kwargs))
        return None

    def my_replies(self, uid):
        rs = self.filter(Q(uid=uid) | Q(reply_to=uid)).order_by('created')
        if rs:
            pass
        logging.info('Not found replies for: {}'.format(uid))
        return None


reply_service = ReplyService()

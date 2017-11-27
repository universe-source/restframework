"""
group基本操作
"""
from django.contrib.auth.models import Group
from customs import BaseService
from ..serializers import GroupSerializer


class GroupService(BaseService):
    model = Group
    serializer_class = GroupSerializer
    desc = 'Person object serializes'

    def serialize(self, obj, context=None):
        """序列化某一个单一对象"""
        context = {'desc': self.desc} if not context else context
        return self.serializer_class(obj, context=context).data

    def serializes(self, objs, context=None):
        """序列化某一个对象列表"""
        return [self.serialize(obj, context=context) for obj in objs]


group_service = GroupService()

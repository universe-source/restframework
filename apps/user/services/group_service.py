"""
group基本操作
"""
from django.contrib.auth.models import Group
from customs import BaseService, BaseSerializer
from ..serializers import GroupSerializer


class GroupService(BaseService, BaseSerializer):
    model = Group
    serializer_class = GroupSerializer
    desc = 'Person object serializes'


group_service = GroupService()

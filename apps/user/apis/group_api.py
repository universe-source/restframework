from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

from customs import SimpleResponse
from ..serializers import GroupSerializer
from ..services import group_service


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def list(self, request):
        return SimpleResponse(group_service.serializes(self.queryset))

    def retrieve(self, request, gid):
        group = get_object_or_404(self.queryset, id=gid)
        return SimpleResponse(group_service.serialize(group))

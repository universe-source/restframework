"""
    After routing has determined which controller to user for a request,
    your controller is responsible for making sense of the request and producing
    the appropriate output.
"""
#  from django.shortcuts import render
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Person
from .serializers import PersonSerializer, GroupSerializer


class PersonViewSet(viewsets.ViewSet):
    """
    Typically, rather than explicitly registering the views in a viewsets in the urlconf,
    you'll register the viewset with a router class, that automatically determines the 
    urlconf for you.
    """
    queryset = Person.objects.all().order_by('-user__date_joined')
    serializer_class = PersonSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def serialize(self, user):
        """序列化某一个单一对象"""
        return self.serializer_class(user).data

    def serialize_objs(self, objs):
        """序列化某一个对象列表"""
        return [self.serialize(obj) for obj in objs]

    def list(self, request):
        return Response(self.serialize_objs(self.queryset))

    def retrieve(self, request, id):
        """
        关于django onetooneField, 必须确保relationFields是一致的.
        Person表虽然会创建id字段, 但是查询时应该使用user_id
        """
        person = Person.objects.get(user__id=id)
        user = get_object_or_404(self.queryset, user__id=id)
        return Response(self.serialize(user))


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def serialize(self, user):
        """序列化某一个单一对象"""
        return self.serializer_class(user).data

    def serialize_objs(self, objs):
        """序列化某一个对象列表"""
        return [self.serialize(obj) for obj in objs]

    def list(self, request):
        return Response(self.serialize_objs(self.queryset))

    def retrieve(self, request, id):
        user = get_object_or_404(self.queryset, id=id)
        return Response(self.serialize(user))

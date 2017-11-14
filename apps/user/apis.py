"""
    After routing has determined which controller to user for a request,
    your controller is responsible for making sense of the request and producing
    the appropriate output.
"""
#  from django.shortcuts import render
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from customs import model_update, SimpleResponse

from .models import Person
from .serializers import PersonSerializer, GroupSerializer


class PersonViewSet(viewsets.ViewSet):
    """
    Typically, rather than explicitly registering the views in a viewsets in the urlconf,
    you'll register the viewset with a router class, that automatically determines the 
    urlconf for you.
    """
    # 用于下面的list接口, 如果 API 中没有使用到queryset, 那么实际上不会产生任何效果
    # PS: 如果在程序运行一段时间之后, 利用 SQL 在用户表中增加一个新用户, 则因为缓存
    #       可能不会返回
    queryset = Person.objects.all().order_by('-user__date_joined')
    serializer_class = PersonSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    permission_classes = []

    def serialize(self, user):
        """序列化某一个单一对象"""
        return self.serializer_class(user).data

    def serialize_objs(self, objs):
        """序列化某一个对象列表"""
        return [self.serialize(obj) for obj in objs]

    def list(self, request):
        """
        desc: list all user
        parameters:
        - name: nickname
            type: string
            location: query
        - name: email
            type: string
            location: query
        """
        print('Query:', request.query_params)
        filter_query = {}
        if 'nickname' in request.query_params:
            filter_query['nickname__icontains'] = request.query_params['nickname']
        if 'email' in request.query_params:
            filter_query['email__icontains'] = request.query_params['email']

        return SimpleResponse(self.serialize_objs(self.queryset.filter(**filter_query)))

    def retrieve(self, request, id):
        """关于django onetooneField, 必须确保relationFields是一致的.
        Person表虽然会创建id字段, 但是查询时应该使用user_id
        """
        #  person = Person.objects.get(user__id=id)
        person = get_object_or_404(self.queryset, id=id)
        return SimpleResponse(self.serialize(person))

    def update(self, request, id):
        """
        desc: update a user
        parameters:
            - name: body
              paramType: body
              required: True
              location: body
        Example Request:
            {
                "user": {
                    "first_name": "我是first",
                    "last_name": "我是last"
                },
                "age": 8
            }
        """
        person = get_object_or_404(self.queryset, id=id)
        user_params = request.data.pop('user', {})
        person_params = {}
        for key in ('age', ):
            if key in request.data:
                person_params[key] = request.data.get(key)
        model_update(person.user, **user_params)
        person.update(**person_params)

        return SimpleResponse(self.serialize(person))


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
        return SimpleResponse(self.serialize_objs(self.queryset))

    def retrieve(self, request, id):
        group = get_object_or_404(self.queryset, id=id)
        return SimpleResponse(self.serialize(group))

"""
    After routing has determined which controller to user for a request,
    your controller is responsible for making sense of the request and producing
    the appropriate output.
"""
#  from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout as _logout, login as _login
from rest_condition import Or
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import list_route

import errors
from customs.permissions import AllowPostPermission
from customs import model_update, SimpleResponse, filter_params
from apps.config import SESSION_KEY
from ..permissions import login_required, admin_required, is_user_self
from ..models import Person
from ..serializers import PersonSerializer
from ..services import person_service, token_service, session_service


class PersonViewSet(viewsets.ViewSet):
    """
    Typically, rather than explicitly registering the views in a viewsets in
    the urlconf, you'll register the viewset with a router class, that automatically
    determines the urlconf for you.
    """
    # queryset: 用于list接口, 如果 API 中没有使用到queryset, 那么实际上不会产生任何效果
    # PS: 如果在程序运行一段时间之后, 利用 SQL 在用户表中增加一个新用户, 则因为缓存
    #       可能不会返回
    queryset = Person.objects.all().order_by('-user__date_joined')
    serializer_class = PersonSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    # 匿名用户只读, 更新则需要登录
    permission_classes = [
        Or(permissions.IsAuthenticatedOrReadOnly, AllowPostPermission, )]

    @admin_required
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
        filter_query = {}
        if 'nickname' in request.query_params:
            filter_query['nickname__icontains'] = request.query_params['nickname']
        if 'email' in request.query_params:
            filter_query['email__icontains'] = request.query_params['email']

        objs = self.queryset.filter(**filter_query)
        return SimpleResponse(person_service.serializes(objs))

    @is_user_self
    def retrieve(self, request, pk):
        """关于django onetooneField, 必须确保relationFields是一致的.
        Person表虽然会创建id字段, 但是查询时应该使用user_id
        """
        if False and 'sessionid' in request.COOKIES:
            # 方式1: 将这段代码移动到装饰器中, 进行用户的验证, 其中sessdata包含uid信息
            # 利用get_decoded()来获取uid和过期, 从而确认用户是否拥有权限
            sessionid = request.COOKIES.get('sessionid')
            print('Cookie sessionid: ', sessionid)
            session = session_service.get_or_none(pk=sessionid)
            print('Session Value:', session)
        person = get_object_or_404(self.queryset, id=pk)
        return SimpleResponse(person_service.serialize(person))

    def update(self, request, pk):
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
                "age": 8,
                "nickname": "ni1",
                "gender": "M",
                "birthday": "2018-01-01"
            }
        """
        person = get_object_or_404(self.queryset, id=pk)

        user_params = filter_params(
            request.data.pop('user', {}), ('first_name', 'last_name'))
        person_params = filter_params(
            request.data, ('age', 'nickname', 'gender', 'birthday'))

        model_update(person.user, **user_params)
        person.update(**person_params)

        return SimpleResponse(person_service.serialize(person))

    @list_route(methods=['post'])
    def login(self, request):
        """
        desc: login
        parameters:
            - name: body
              paramType: body
              required: True
              location: body
        Example Request:
            {
                "username": "xxxx",
                "password": "xxxx",
            }
            or
            {
                "token": "key"
            }
        """
        username = request.data.get('username')
        password = request.data.get('password')
        token = request.data.get('token')
        person = None
        if username and password:
            person = person_service.login(username, password)
        elif token:
            person = person_service.auth(token)
        if person:
            # 方式1: 生成一个session key并存储到数据库中, django自动进行 SQL 操作
            # 方式2: 使用rest framework 自带的session
            #  request.session[SESSION_KEY] = person.id
            _login(request, person.user)
            data = person_service.serialize(person)
            data['token'] = token_service.serialize(person.token)
            return SimpleResponse(data=data)
        return SimpleResponse(code=errors.CODE_CHECK_PASSWD_FAILED)

    @list_route(methods=['get'])
    @login_required
    def logout(self, request):
        """
        desc: logout
        """
        # 对应login中的_authenticate方法, 会自动将session_key删除
        _logout(request)
        person_service.logout(request.user)
        return SimpleResponse(code=errors.CODE_SUCCESSFUL)

    @list_route(methods=['put'])
    @login_required
    def defer(self, request):
        """
        desc: defer token expired
        """
        succ = person_service.defer(request.user)
        if succ:
            return SimpleResponse(code=errors.CODE_SUCCESSFUL)
        return SimpleResponse(code=errors.CODE_FAILED)

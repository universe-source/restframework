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
from customs import SimpleResponse, filter_params
from ..permissions import login_required, admin_required, is_user_self
from ..models import Person
from ..serializers import PersonSerializer
from ..services import person_service, token_service, session_service
from ..params import check_params


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
                "first_name": "我是first",
                "last_name": "我是last"
                "age": 8,
                "nickname": "ni1",
                "gender": "M",
                "birthday": "2018-01-01"
            }
        """
        person = get_object_or_404(self.queryset, id=pk)

        person_params = filter_params(
            request.data, ('age', 'nickname', 'gender', 'birthday',
                           'first_name', 'last_name'))
        person.update(**person_params)

        return SimpleResponse(person_service.serialize(person))

    @list_route(methods=['post', 'get'])
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
            GET url?token=key
        """
        if request.method == 'GET':
            token = request.query_params.get('token')
            person = person_service.auth(token)
            if person:
                return SimpleResponse(data=person_service.serialize(person))
            return SimpleResponse(code=errors.CODE_BAD_TOKEN)
        elif request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')
            person = None
            person = person_service.login(username, password)
            if person:
                # 方式1: 生成一个session key并存储到数据库中, django自动进行 SQL 操作
                # 方式2: 使用rest framework 自带的session
                #  from apps.config import SESSION_KEY
                #  request.session[SESSION_KEY] = person.id
                _login(request, person)
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

    @list_route(methods=['post'])
    def register(self, request):
        """
        desc: register
        parameters:
            - name: body
              paramType: body
              required: True
              location: body
        Example Request:
            {
                "username": "xxxx",
                "email": "bifeng@163.com",
                "password": "xxxx",
            }
        """
        succ, kwargs = check_params(request.data, ('username', 'password', 'email'))
        if succ:
            kwargs.update(filter_params(
                request.data, ('nickname', 'age', 'gender', 'country_code',
                               'province', 'birthday', 'first_name', 'last_name')
            ))
            succ, person = person_service.register(
                kwargs.pop('username'), kwargs.pop('password'), **kwargs)
            if succ:
                token = token_service.get_or_none(uid=person.id)
                if token:
                    data = person_service.serialize(person)
                    data['token'] = token_service.serialize(token)
                    data['sign'] = person.sign
                    return SimpleResponse(data=data)
                return SimpleResponse(code=errors.CODE_UNEXIST_TOKEN)
            return SimpleResponse(code=person)
        return SimpleResponse(message='Leak of keys:{}'.format(kwargs))

    @list_route(methods=['get'])
    def validate(self, request):
        """
        desc: validate sign
        parameters:
        - name: sign
            type: string
            location: query
        """
        sign = request.query_params.get('sign')
        if sign:
            succ, person = person_service.validate(sign)
            if succ:
                token = token_service.get_or_none(uid=person.id)
                if token:
                    data = person_service.serialize(person)
                    data['token'] = token_service.serialize(token)
                    return SimpleResponse(data=data)
                return SimpleResponse(code=errors.CODE_UNEXIST_TOKEN)
            return SimpleResponse(code=person)
        return SimpleResponse(code=errors.CODE_BAD_ARGUMENT)

    @list_route(methods=['put'])
    @login_required
    def defer(self, request):
        """
        desc: defer token expired
        """
        succ = token_service.defer(request.user)
        if succ:
            return SimpleResponse(code=errors.CODE_SUCCESSFUL)
        return SimpleResponse(code=errors.CODE_FAILED)

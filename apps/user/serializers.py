from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Person, AuthToken


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class PersonSerializer(serializers.ModelSerializer):
    """Person相当于对 User 进行封装"""
    # 更改返回的key
    created = serializers.SerializerMethodField('get_date_joined')
    updated = serializers.SerializerMethodField('get_last_login')

    class Meta:
        model = Person
        exclude = ('is_superuser', 'password', 'last_login', 'date_joined',
                   'is_staff', 'groups', 'user_permissions')

    def get_date_joined(self, obj):
        return obj.date_joined

    def get_last_login(self, obj):
        return obj.last_login


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        exclude = ('updated', 'created')
        #  fields = '__all__'  # 显示所有字段, 不能和exclude连用

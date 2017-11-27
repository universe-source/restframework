from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Person, AuthToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('id', 'is_staff', 'password', 'last_login', 'is_superuser',
                   'is_active', 'groups', 'user_permissions')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class PersonSerializer(serializers.ModelSerializer):
    """Person相当于对 User 进行封装"""
    user = UserSerializer()

    class Meta:
        model = Person
        exclude = ('updated', 'created')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        exclude = ('updated', 'created')
        #  fields = '__all__'  # 显示所有字段, 不能和exclude连用

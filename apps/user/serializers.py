from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Person, AuthToken


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class PersonSerializer(serializers.ModelSerializer):
    """Person相当于对 User 进行封装"""
    class Meta:
        model = Person
        exclude = ('id', 'is_superuser', 'password', 'last_login', 'updated', 'created')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        exclude = ('updated', 'created')
        #  fields = '__all__'  # 显示所有字段, 不能和exclude连用

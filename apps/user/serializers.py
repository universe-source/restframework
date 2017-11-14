from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Person


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #  exclude = ('is_staff', )
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class PersonSerializer(serializers.ModelSerializer):
    """Person相当于对 User 进行封装"""
    user = UserSerializer()

    class Meta:
        model = Person
        fields = ('user', 'age', 'updated', 'created')

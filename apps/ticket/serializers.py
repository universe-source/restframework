"""
Serialize all ticket model
"""
from rest_framework import serializers
from .models import TicketTask, TicketType, TicketOperate, TicketNode


class TicketTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTask
        fields = '__all__'


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'


class TicketOperateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketOperate
        fields = '__all__'


class TicketNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketNode
        fields = '__all__'

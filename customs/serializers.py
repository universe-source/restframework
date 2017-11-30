from rest_framework import serializers


class BaseSerializer(object):
    serializer_class = serializers.Serializer
    desc = ''

    def serialize(self, obj, context=None):
        """序列化某一个单一对象"""
        context = {'desc': self.desc} if not context else context
        return self.serializer_class(obj, context=context).data

    def serializes(self, objs):
        """序列化某一个对象列表"""
        return [self.serialize(obj) for obj in objs]

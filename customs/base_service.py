"""
基础数据库类.
Django Version: 1.11
"""


class BaseService(object):
    ''' Base CURD operation '''
    model = None

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def bulk_create(self, objs, batch_size=None):
        return self.model.objects.bulk_create(objs, batch_size)

    def get(self, **kwargs):
        return self.model.objects.get(**kwargs)

    def get_or_create(self, default=None, **kwargs):
        """look https://docs.djangoproject.com/en/1.11/ref/models/querysets/
        @return: obj, created
        """
        return self.model.objects.get_or_create(default, **kwargs)

    def get_or_none(self, **kwargs):
        try:
            return self.model.objects.get(**kwargs)
        except Exception:
            return None

    def filter(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def update(self, object_or_queryset, **kwargs):
        return object_or_queryset.update(**kwargs)

    def update_or_create(self, default=None, **kwargs):
        """look https://docs.djangoproject.com/en/1.11/ref/models/querysets/
        @return: obj, created
        """
        return self.model.object.update_or_create(default, **kwargs)

    def delete(self, object_or_queryset):
        if getattr(self.model, 'deleted', None) is not None:
            return object_or_queryset.update(deleted=True)
        return object_or_queryset.delete()

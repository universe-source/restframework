from django.db import models
from django.conf import settings


def model_update(obj, **kwargs):
    fields = {}
    values = {}

    for f in obj._meta.fields:
        fields[f.name] = f
    for k, v in kwargs.items():
        if k in fields:
            values[k] = v
    if values:
        obj.__dict__.update(**values)
        obj.save()
    return obj


class UpdateTable(object):
    def update(self, **kwargs):
        return model_update(self, **kwargs)

    class Meta:
        abstract = True


class CacheableQuerySet(models.QuerySet):
    """自定义查询集, 添加额外的querset方法, 配合CacheableManager中的get_queryset使用"""
    def is_cacheable(self):
        if settings.CACHE_QUERY:
            return getattr(self.model, 'CACHEABLE', True)
        return False


class XManager(models.Manager):
    """
    @function: 管理器, 对model对象的操作, 增加表级功能
    @Note: 对于get等非queryset是不存在缓存的, filter则有自带的内部缓存
    @optimize: 对于大数据的filter, queryset可能造成巨大的内存浪费, 使用exists/iterator
    """
    def get_queryset(self):
        if getattr(self, 'queryset', None) is None:
            return CacheableQuerySet(self.model, using=self._db)
        return self.queryset

    def get_or_none(self, *args, **kwargs):
        try:
            obj = self.get(*args, **kwargs)
            return obj
        except Exception as msg:
            print('Exception:', msg)
            return None

    def update_or_create(self, defaults=None, **kwargs):
        try:
            obj = self.get(**kwargs)
            if defaults:
                obj.update(**defaults)
            return obj, False
        except Exception:
            if defaults:
                kwargs.update(defaults)
            return self.create(**kwargs), True


class CacheableManager(XManager):
    """cacheops 缓冲"""
    pass


class UnCacheableManager(XManager):
    """
    基于cacheops, 不适用缓存来进行操作, 并非真正意义上的非缓存, queryset自带就有缓存
    """
    def all(self):
        queryset = self.get_queryset()
        objs = queryset.all().nocache()
        return objs

    def filter(self, *args, **kwargs):
        return self.get_queryset().filter(*args, **kwargs).nocache()


class DateTimeModel(models.Model):
    """ A base model with created and edited datetime fields """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

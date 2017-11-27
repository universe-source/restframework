from django.db import models


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


class CacheableManager(models.Manager):
    def get_or_none(self, *args, **kwargs):
        try:
            obj = self.get(*args, **kwargs)
            return obj
        except Exception:
            return None


class DateTimeModel(models.Model):
    """ A base model with created and edited datetime fields """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

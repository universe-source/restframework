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

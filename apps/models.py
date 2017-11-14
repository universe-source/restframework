"""
Basic Model Class
"""
from django.db import models


class DateTimeModel(models.Model):
    """ A base model with created and edited datetime fields """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

from django.dispatch import receiver
from django.db import models
from .models import AuthToken


@receiver(models.signals.post_save, sender='user.Person')
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and instance is not None:
        AuthToken.objects.create(uid=instance.id)

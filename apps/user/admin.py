from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Person


class PersonInline(admin.StackedInline):
    """添加该类以便在django自带的管理后台控制 Person """
    model = Person
    can_delete = False
    verbose_name_plural = 'person'


class PersonAdmin(UserAdmin):
    # Define a new User admin
    inlines = (PersonInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, PersonAdmin)

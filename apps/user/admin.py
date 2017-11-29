from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import Person


class PersonChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Person


class PersonAdmin(UserAdmin):
    """参考: https://stackoverflow.com/questions/15012235/using-django-auth-useradmin-for-a-custom-user-model
    """
    form = PersonChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', )}),
    )


# Re-register UserAdmin
admin.site.register(Person, PersonAdmin)

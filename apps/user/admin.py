"""
Custome User之后的操作步骤:
    1 确保custom user能够顺利的创建
    2 创建 CustomUserManager, 见文件apps/user/managers.py
    3 删除所有admin后台的插件(避免这些因素导致无法正常登陆)
    4 编写下面的代码
    5 测试登录
    6 测试创建
"""
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm, ReadOnlyPasswordHashField)

from .models import Person


class PersonChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()

    class Meta(UserChangeForm.Meta):
        model = Person
        fields = ('username', 'email', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]


class PersonCreationForm(UserCreationForm):
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = Person
        fields = ('username', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            Person.objects.get(username=username)
        except Person.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(PersonCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PersonAdmin(UserAdmin):
    """参考: https://stackoverflow.com/questions/15012235/using-django-auth-useradmin-for-a-custom-user-model
    """
    form = PersonChangeForm
    add_form = PersonCreationForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'age', 'gender', 'birthday', 'country_code')}),
    )


# Re-register UserAdmin
admin.site.register(Person, PersonAdmin)

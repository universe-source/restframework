"""
Setting for REST Frawework of our projects.
"""


class RestConfig(object):
    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
            # 默认的权限控制,  如果没有覆盖则生效
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
            'rest_framework.permissions.IsAdminUser',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'customs.authentications.XTokenAuthentication',
        ),
        # 如果存在, 则会自动进行分页
        'PAGE_SIZE': 10,
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    }

    # 调用rest_framework.urls来进行用户的登录登出
    # Reference: https://django-rest-swagger.readthedocs.io/en/latest/settings/
    LOGIN_URL = 'rest_framework:login'
    LOGOUT_URL = 'rest_framework:logout'

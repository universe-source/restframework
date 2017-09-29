"""
Setting for REST Frawework of our projects.
"""


class RestConfig(object):
    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
            #  'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
            'rest_framework.permissions.IsAdminUser',
        ],
        # 如果存在, 则会自动进行分页
        'PAGE_SIZE': 10,
    }

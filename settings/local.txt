"""
    Local configuration
"""
from .common import Common


class Local(Common):
    DEBUG = True
    SETTING = 'Local'

    # CACHE Open/Close
    CACHE_QUERY = True

    # Database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'shop',
            'USER': 'shop',
            'PASSWORD': 'shop@297413',
            'HOST': '127.0.0.1',
            # Set to empty string for default. Not used with sqlite3.
            #  'PORT': '3357',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
    # End database configuration

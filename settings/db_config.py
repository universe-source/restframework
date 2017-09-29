"""
Django setting of db, cache(redis), queue
"""
import os


class DBConfig(object):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

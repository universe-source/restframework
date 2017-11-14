"""
Django setting of log
"""
import os


class LogConfig(object):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': ("%(levelname)s %(asctime)s %(module)s "
                           "%(filename)s:%(lineno)s "
                           "%(process)d %(thread)d %(message)s")
            },
        },
        'filters': {},
        'handlers': {
            'error': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/error.log'),
                'formatter': 'verbose'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['error'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
    DEBUG_LOGGERS = ['user']
    for name in DEBUG_LOGGERS:
        handler = {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/%s.log' % name),
            'formatter': 'verbose'
        }
        logger = {
            'handlers': [name],
            'level': 'INFO',
            'propagate': True,
        }
        LOGGING['handlers'][name] = handler
        LOGGING['loggers'][name] = logger
    # END LOGGING CONFIGURATION

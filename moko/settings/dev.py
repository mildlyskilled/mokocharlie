from base import *
import django.conf.global_settings as default_settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ENABLE_NEW_RELIC = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/moko.log'),
            'formatter': 'simple',
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/requests.log'),
            'formatter': 'verbose',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# override facebook settings

SOCIAL_AUTH_FACEBOOK_KEY = "376334572402987"
SOCIAL_AUTH_FACEBOOK_SECRET = "5ebd62c909c9d9f9d3b512b8e7078d53"

DEBUG_TOOLBAR_PATCH_SETTINGS = False
TEMPLATE_DEBUG = True
INSTALLED_APPS += (
    'debug_toolbar',
)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ADMIN_EMAIL = "kwabena.aning@gmail.com"


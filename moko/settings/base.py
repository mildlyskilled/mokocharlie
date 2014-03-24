import sys
import urlparse

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pqu+!+4e==a0#=n(z$1b21iyalhh^5#%axb#$e!ga61*-8w!(l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photos',
    'cloudinary',
    'crispy_forms',
    'django_gravatar',
    'social.apps.django_app.default',
    'endless_pagination',
    'south',
    'common'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.moko_social.MokoSocialMiddleWare',
)

ROOT_URLCONF = 'moko.urls'

WSGI_APPLICATION = 'moko.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
    }
}


# Register database schemes in URLs.
urlparse.uses_netloc.append('mysql')

try:

    # Check to make sure DATABASES is set in settings.py file.
    # If not default to {}

    if 'DATABASES' not in locals():
        DATABASES = {}

    if 'DATABASE_URL' in os.environ:
        url = urlparse.urlparse(os.environ['DATABASE_URL'])

        # Ensure default database exists.
        DATABASES['default'] = DATABASES.get('default', {})

        # Update with environment configuration.
        DATABASES['default'].update({
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })


        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
except Exception:
    print 'Unexpected error:', sys.exc_info()



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, '../templates')
)

# Cloudinary settings for Django. Add to your settings file.
CLOUDINARY = {
  'cloud_name': 'hv52shllz',
  'api_key': '211234747938451',
  'api_secret': 'ATmGWjd4_UyVsC9vwTfLqI_xzx0',
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_REDIRECT_URL = "/profile"
LOGIN_URL = '/login/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

SOCIAL_AUTH_TWITTER_KEY = "bqOTvdYoySztq1ylQFqzw"
SOCIAL_AUTH_TWITTER_SECRET = "STWqPpO0O02vKptUpiNrYsHpgrj1HMExtPn3xhf336I"

SOCIAL_AUTH_FACEBOOK_KEY = "81700851985"
SOCIAL_AUTH_FACEBOOK_SECRET = "1abaa53b4babeb3c860506d8f57e577a"

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = "77esqvhx7ukhea"
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = "ICfanfvnlIjY7o3N"
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_emailaddress', 'r_basicprofile']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address',]
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('email-address', 'email_address')]

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', ]

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/profile/"
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = "/profile/"

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.linkedin.LinkedinOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.google.GooglePlusAuth',
    'social.backends.email.EmailAuth',
    'django.contrib.auth.backends.ModelBackend',
)

# pagination settings
ENDLESS_PAGINATION_PER_PAGE = 20
ENDLESS_PAGINATION_PREVIOUS_LABEL = '<i class="glyphicon glyphicon-chevron-left"></i>'
ENDLESS_PAGINATION_NEXT_LABEL = '<i class="glyphicon glyphicon-chevron-right"></i>'
ENDLESS_PAGINATION_PAGE_LIST_CALLABLE = 'endless_pagination.utils.get_elastic_page_numbers'

AUTH_USER_MODEL = 'common.MokoUser'
EMAIL_FROM = "info@mokocharlie.com"

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)
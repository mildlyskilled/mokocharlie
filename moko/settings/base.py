import sys
import urlparse

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pqu+!+4e==a0#=n(z$1b21iyalhh^5#%axb#$e!ga61*-8w!(l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'haystack',
    'photos',
    'ipware',
    'cloudinary',
    'crispy_forms',
    'django_gravatar',
    'social.apps.django_app.default',
    'endless_pagination',
    'south',
    'common',
    'common',
    'classifieds',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'common.middleware.moko_social.MokoSocialMiddleWare',
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

# Test database

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


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
    'common.context_processors.photo_count',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

SOCIAL_AUTH_TWITTER_KEY = "bqOTvdYoySztq1ylQFqzw"
SOCIAL_AUTH_TWITTER_SECRET = "STWqPpO0O02vKptUpiNrYsHpgrj1HMExtPn3xhf336I"

SOCIAL_AUTH_FACEBOOK_KEY = "81700851985"
SOCIAL_AUTH_FACEBOOK_SECRET = "1abaa53b4babeb3c860506d8f57e577a"

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = "77esqvhx7ukhea"
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = "ICfanfvnlIjY7o3N"
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['id', 'email-address', 'first-name', 'last-name']
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('id', 'id'),
                                          ('first-name', 'first_name'),
                                          ('last-name', 'last_name'),
                                          ('email-address', 'email_address')]

#SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', ]

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
    'social.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'

)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect'
)

# you can provide your own meta precedence order by
# including IPWARE_META_PRECEDENCE_ORDER in your
# settings.py. The check is done from top to bottom
IPWARE_META_PRECEDENCE_LIST = (
    'HTTP_X_FORWARDED_FOR',  # client, proxy1, proxy2
    'HTTP_CLIENT_IP',
    'HTTP_X_REAL_IP',
    'HTTP_X_FORWARDED',
    'HTTP_X_CLUSTER_CLIENT_IP',
    'HTTP_FORWARDED_FOR',
    'HTTP_FORWARDED',
    'HTTP_VIA',
    'REMOTE_ADDR',
)

# you can provide your own private IP prefixes by
# including IPWARE_PRIVATE_IP_PREFIX in your setting.py
# IPs that start with items listed below are ignored
# and are not considered a `real` IP address
IPWARE_PRIVATE_IP_PREFIX = (
                               '0.', '1.', '2.',  # externally non-routable
                               '10.',  # class A private block
                               '169.254.',  # link-local block
                               '172.16.', '172.17.', '172.18.', '172.19.',
                               '172.20.', '172.21.', '172.22.', '172.23.',
                               '172.24.', '172.25.', '172.26.', '172.27.',
                               '172.28.', '172.29.', '172.30.', '172.31.',  # class B private blocks
                               '192.0.2.',  # reserved for documentation and example code
                               '192.168.',  # class C private block
                               '255.255.255.',  # IPv4 broadcast address
                           ) + (  # the following addresses MUST be in lowercase)
                                  '2001:db8:',  # reserved for documentation and example code
                                  'fc00:',  # IPv6 private block
                                  'fe80:',  # link-local unicast
                                  'ff00:',  # IPv6 multicast
                           )

CLOUDINARY_TRANSFORMATIONS = [
    ("LARGE_COMMENT_PREVIEW", "comment_image_pre"),
    ("SMALL_COMMENT_PREVIEW", "comment_image_thumbnail"),
    ("IMAGE_THUMBNAIL_PREVIEW", "image_preview"),
    ("ALBUM_COVER_PREVIEW", "album_preview"),
    ("MAIN_IMAGE_VIEW", "moko_resize_730_l")
]

YOUTUBE_AUTH_EMAIL = '118063279160-9qge7douhfnghrn3dk8qnthfiglp5thl@developer.gserviceaccount.com'
YOUTUBE_AUTH_PASSWORD = 'q89dYpx3d5QZ4tsFnvNnMaUE'
YOUTUBE_DEVELOPER_KEY = 'AI39si5h_BDa5OGCp_pKdm394xA0f2kwnwQrXVQL_fLI0bG78nUC0YgJvrCc-lrShyB5qsDBpmRa7WwZK1XbrLgGyeFHG4os8g'
YOUTUBE_CLIENT_ID = '118063279160-9qge7douhfnghrn3dk8qnthfiglp5thl.apps.googleusercontent.com'
YOUTUBE_UPLOAD_REDIRECT_URL = '/youtube/videos/'
YOUTUBE_DELETE_REDIRECT_URL = '/video/'

if 'SEARCHBOX_SSL_URL' in os.environ:
    search_box_elastic_search_url = os.environ['SEARCHBOX_SSL_URL']
else:
    search_box_elastic_search_url = 'https://paas:d4b18f626b95e75fdac571b738cbb402@dwalin-us-east-1.searchly.com'

if 'BONSAI_URL' in os.environ:
    bonsai_url = os.environ['BONSAI_URL']
else:
    bonsai_url = 'https://np2fdvyv:4m0v2p37cknwe7js@box-4649745.us-east-1.bonsai.io/'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': search_box_elastic_search_url,
        'INDEX_NAME': 'mokocharlie',
    },
}

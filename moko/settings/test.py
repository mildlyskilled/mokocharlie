from base import *
import os

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, '../data/tests.sqlite3'),
    'TEST': {'NAME': os.path.join(BASE_DIR, '../data/tests.sqlite3')}
}

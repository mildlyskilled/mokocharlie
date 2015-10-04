import os
from dj_static import Cling
from django.core.wsgi import get_wsgi_application
from django.conf import settings

if settings.ENABLE_NEW_RELIC:
    import newrelic.agent
    newrelic.agent.initialize(environment=settings.ENV)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moko.settings")
application = Cling(get_wsgi_application())

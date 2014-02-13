from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'moko.views.home', name='home'),
                       (r'^photos', include('photos.urls')),
                       (r'^photos/', include('photos.urls', namespace='photos')),
                       (r'^admin/', include(admin.site.urls)),
)
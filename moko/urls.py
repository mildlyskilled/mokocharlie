from django.conf.urls import patterns, include, url
from django.contrib import admin
from moko.views import HomeViewTemplate

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', HomeViewTemplate.as_view()),
                       (r'^photos', include('photos.urls')),
                       (r'^photos/', include('photos.urls', namespace='photos')),
                       (r'^albums', include('albums.urls')),
                       (r'^albums/', include('albums.urls', namespace='albums')),
                       (r'^admin/', include(admin.site.urls)),
)
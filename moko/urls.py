from django.conf.urls import patterns, include, url
from django.contrib import admin
from photos.views import *
from moko.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', HomeViewTemplate.as_view()),
                       # Photo Endpoints
                       url(r'^photos/$', PhotosTemplate.as_view(), name="photo_list"),
                       url(r'^photos/view/(?P<image_id>\w+)/$', PhotoViewTemplate.as_view(), name='image_view'),
                       # Album endpoints
                       url(r'^albums', AlbumTemplate.as_view(), name='album_list'),
                       url(r'^albums/view/(?P<album_id>\w+)/$', AlbumViewTemplate.as_view(), name='album_view'),

                       # Admin endpoints
                       (r'^admin/', include(admin.site.urls)),
)
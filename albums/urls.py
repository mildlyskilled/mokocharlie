from django.conf.urls import patterns, url
from albums.views import AlbumTemplate, AlbumViewTemplate

urlpatterns = patterns('',
                       url(r'^/$', AlbumTemplate.as_view(), name="album_list"),
                       url(r'^/view/(?P<album_id>\w+)/$', AlbumViewTemplate.as_view(), name='album_view'),
)
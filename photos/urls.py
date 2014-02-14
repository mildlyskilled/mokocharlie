from django.conf.urls import patterns, url
from photos.views import PhotosTemplate, PhotoViewTemplate

urlpatterns = patterns('',
                       url(r'^/$', PhotosTemplate.as_view()),
                       url(r'^/view/(?P<image_id>\w+)/$', PhotoViewTemplate.as_view(), name='image_view'),
)
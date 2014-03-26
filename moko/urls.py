from django.conf.urls import patterns, include, url
from django.contrib import admin
from photos.views import *
from moko.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', HomeViewTemplate.as_view()),
                       # Authentication
                       url(r'^login/$', LoginViewTemplate.as_view(), name='login'),
                       url(r'^logout/$',LogoutViewTemplate.as_view(), name='logout'),

                       # Accounts
                       url(r'^profile/$', ProfileViewTemplate.as_view(), name='profile'),
                       url(r'^profile/new$', ExtraDetailsViewTemplate.as_view(), name='new_profile'),
                       # Photo Endpoints
                       url(r'^photos/$', PhotosTemplate.as_view(), name="photo_list"),
                       url(r'^photos/view/(?P<image_id>\d+)/$', PhotoViewTemplate.as_view(), name='photo_view'),
                       # Album endpoints
                       url(r'^albums/$', AlbumTemplate.as_view(), name='album_list'),
                       url(r'^albums/view/(?P<album_id>\d+)/$', AlbumViewTemplate.as_view(), name='album_view'),
                       # Comments endpoints
                       # AJAX endpoint for comment form
                       url(r'^comments/new_form/$', NewCommentViewTemplate.as_view(), name='comment_form'),
                       url(r'^comments/$', CommentListViewTemplate.as_view(), name='comment_list'),
                       # Favouriting photos
                       #AJAX endpoint for favouriting a photo
                       url(r'^photos/favourite/(?P<photo_id>\d+)/$', FavouritePhotoViewTemplate.as_view(), name='favourite_photo'),
                       # Admin endpoints
                       (r'^admin/', include(admin.site.urls)),
                       # Social logins
                        url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
)
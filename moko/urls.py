from django.conf.urls import patterns, include, url
from django.contrib import admin
from haystack.views import (SearchView, search_view_factory)
from moko.forms import GeneralSearchForm
from photos.views import *
from moko.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', HomeViewTemplate.as_view(), name='home'),
                       # Authentication
                       url(r'^login/$', LoginViewTemplate.as_view(), name='login'),
                       url(r'^logout/$', LogoutViewTemplate.as_view(), name='logout'),

                       # Accounts
                       url(r'^profile/$', ProfileViewTemplate.as_view(), name='profile'),
                       url(r'^profile/new$', ExtraDetailsViewTemplate.as_view(), name='new_profile'),
                       # Photo Endpoints
                       url(r'^photos/$', PhotosTemplate.as_view(), name="photo_list"),
                       url(r'^photos/view/(?P<image_id>\d+)/$', PhotoViewTemplate.as_view(), name='photo_view'),
                       # Album endpoints
                       url(r'^albums/$', AlbumTemplate.as_view(), name='album_list'),
                       url(r'^albums/view/(?P<album_id>\d+)/$', AlbumViewTemplate.as_view(), name='album_view'),
                       # Photo stories
                       url(r'^story/$', StoryIndexViewTemplate.as_view(), name='story_list'),
                       url(r'^story/view/(?P<story_id>\d+)/$', StoryViewTemplate.as_view(), name='story_view'),
                       url(r'^story/view/(?P<story_id>\d+)/(?P<image_id>\d+)/$', StoryViewTemplate.as_view(),
                           name='story_view_with_image'),
                       # Comments endpoints
                       # AJAX endpoint for comment form
                       url(r'^comments/new_form/$', NewCommentViewTemplate.as_view(), name='comment_form'),
                       url(r'^comments/$', CommentListViewTemplate.as_view(), name='comment_list'),
                       # Favouriting photos
                       #AJAX endpoint for favouriting a photo
                       url(r'^photos/favourite/(?P<photo_id>\d+)/$', FavouritePhotoViewTemplate.as_view(),
                           name='favourite_photo'),
                       # Admin endpoints
                       (r'^admin/', include(admin.site.urls)),
                       # Social logins
                       url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
                       # Search endpoints
                       url(r'^search/$', search_view_factory(
                           view_class=SearchView,
                           template='search/search.html',
                           form_class=GeneralSearchForm
                       ), name='haystack_search'),
                       # Hospitality
                       url(r'^hospitality/$', HospitalityTemplate.as_view(), name='hospitality_list'),
                       url(r'^hospitality/(?P<hospitality_id>\d+)$', HospitalityViewTemplate.as_view(),
                           name='hospitality_view'),
)
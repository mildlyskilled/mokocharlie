from django.views.generic.base import TemplateView
from albums.models import *


class AlbumTemplate(TemplateView):
    template_name = "albums/index.html"

    def get_context_data(self, **kwargs):
        albums = Album.objects.all()
        context = super(AlbumTemplate, self).get_context_data()
        context["albums"] = albums
        return context


class AlbumViewTemplate(TemplateView):
    template_name = "albums/view.html"

    def get_context_data(self, **kwargs):
        context = super(AlbumViewTemplate, self).get_context_data()
        context["album"] = Album.objects.get(album_id=self.kwargs.get('album_id'))
        return context
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from albums.models import *
from photos.models import *


class AlbumTemplate(TemplateView):
    template_name = "albums/index.html"
    default_limit = 21
    default_page = 1

    def get_context_data(self, **kwargs):

        albums = Album.objects.all().order_by('-date_added')
        _limit = self.request.GET.get('limit', self.default_limit)
        _page = self.request.GET.get('page', self.default_page)
        p = Paginator(albums, _limit)
        try:
            album_list = p.page(_page)
        except PageNotAnInteger:
            album_list = p.page(self.default_page)
        except EmptyPage:
            album_list = p.page(p.num_pages)

        context = super(AlbumTemplate, self).get_context_data()
        context["albums"] = album_list
        context["paginator_object"] = album_list
        return context


class AlbumViewTemplate(TemplateView):
    template_name = "albums/view.html"
    default_limit = 12
    default_page = 1

    def get_context_data(self, **kwargs):
        album_id = self.kwargs.get('album_id')
        _limit = self.request.GET.get('limit', self.default_limit)
        _page = self.request.GET.get('page', self.default_page)
        album = Album.objects.get(album_id=album_id)

        p = Paginator(Photo.objects.filter(image_album=album_id), _limit)
        try:
            image_list = p.page(_page)
        except PageNotAnInteger:
            image_list = p.page(self.default_page)
        except EmptyPage:
            image_list = p.page(p.num_pages)

        context = super(AlbumViewTemplate, self).get_context_data()
        context["album_images"] = image_list
        context["paginator_object"] = image_list
        context["album"] = album
        return context
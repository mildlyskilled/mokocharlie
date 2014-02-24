from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from moko.models import *
import logging

LOGGER = logging.getLogger(__name__)

class AlbumTemplate(TemplateView):
    template_name = "albums/index.html"
    default_limit = 21
    default_page = 1
    default_order = 'recent'


    def get_context_data(self, **kwargs):

        _limit = self.request.GET.get('limit', self.default_limit)
        _page = self.request.GET.get('page', self.default_page)
        _order = self.request.GET.get('order', self.default_order)


        _order_dict = {'alpha': ['label', 'Alphabetical'],
                       'recent': ['-created_at', 'Most Recent'],
                       'popular': ['-average_views', 'Most Popular']}

        if _order_dict.has_key(_order):
            if _order == 'popular':
                from django.db.models.aggregates import Avg
                albums = Album.objects.annotate(average_views=Avg('photos__times_viewed')).order_by(_order_dict[_order][0]).all()
            else:
                albums = Album.objects.distinct().order_by(_order_dict[_order][0]).all()
        else:
            albums = Album.objects.all()


        LOGGER.debug(albums.query)

        p = Paginator(albums, _limit)
        try:
            album_list = p.page(_page)
        except PageNotAnInteger:
            album_list = p.page(self.default_page)
        except EmptyPage:
            album_list = p.page(p.num_pages)

        comments = Comment.objects.all()[:12]

        context = super(AlbumTemplate, self).get_context_data()
        context["albums"] = album_list
        context["comments"] = comments
        context["order"] = {'selected': _order, 'dictionary': _order_dict}
        return context


class AlbumViewTemplate(TemplateView):
    template_name = "albums/view.html"
    default_limit = 12
    default_page = 1

    def get_context_data(self, **kwargs):
        album_id = self.kwargs.get('album_id')
        _limit = self.request.GET.get('limit', self.default_limit)
        _page = self.request.GET.get('page', self.default_page)
        album = Album.objects.get(id=album_id)

        p = Paginator(album.photos.all(), _limit)
        try:
            image_list = p.page(_page)
        except PageNotAnInteger:
            image_list = p.page(self.default_page)
        except EmptyPage:
            image_list = p.page(p.num_pages)

        # Get comments
        album_comments = Comment.objects.filter(image__album=album_id).order_by('-comment_date')
        # Prepare context
        context = super(AlbumViewTemplate, self).get_context_data()
        context["album_images"] = image_list
        context["paginator_object"] = image_list
        context["album"] = album
        context["album_comments"] = album_comments
        return context
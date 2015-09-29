import logging

from django.views.generic.base import TemplateView
from common.models import *


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
        from collections import OrderedDict

        _order_dict_unsorted = {'alpha': ['label', 'Alphabetical'],
                                'recent': ['-created_at', 'Most Recent'],
                                'popular': ['-average_views', 'Most Popular']}

        if _order in _order_dict_unsorted:
            if _order == 'popular':
                from django.db.models.aggregates import Avg

                albums = Album.objects.annotate(average_views=Avg('photo__times_viewed')).order_by(
                    _order_dict_unsorted[_order][0]).filter(published=1)
            else:
                albums = Album.objects.distinct().order_by(_order_dict_unsorted[_order][0]).filter(published=1)
        else:
            albums = Album.objects.filter(published=1)

        _order_dict = OrderedDict(reversed(sorted(_order_dict_unsorted.items())), key=lambda t: t[0])
        comments = Comment.objects.all().filter(comment_approved=1)[:12]

        context = super(AlbumTemplate, self).get_context_data()
        # TODO set up pagination
        context["albums"] = albums
        context["comments"] = comments
        context["limit"] = _limit
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

        # Get comments
        album_comments = Comment.objects.filter(image__albums=album_id).filter(comment_approved=1).order_by(
            '-comment_date')
        # Prepare context
        context = super(AlbumViewTemplate, self).get_context_data()
        context["album_images"] = album.photo_set.all()
        context["album"] = album
        context["album_comments"] = album_comments
        context["limit"] = _limit
        hospitality = album.hospitality_set.all()
        if hospitality:
            context["hospitality_types"] = " or ".join([h.hospitality_type for h in hospitality])
            context["hospitality_set"] = hospitality

        return context
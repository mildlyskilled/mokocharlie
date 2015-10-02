import logging

from django.views.generic.base import TemplateView
from common.models import *


LOGGER = logging.getLogger(__name__)



class CollectionViewTemplate(TemplateView):
    template_name = "collections/index.html"
    default_limit = 12
    default_page = 1

    def get_context_data(self, **kwargs):
        collection_id = self.kwargs.get('collection_id')
        _limit = self.request.GET.get('limit', self.default_limit)
        _page = self.request.GET.get('page', self.default_page)
        collection = Collection.objects.get(request=collection_id, args=null)

        # Get comments
        collection_comments = Comment.objects.filter(image__albums__collection=collection_id).filter(comment_approved=1).order_by(
            '-comment_date')[:12]
        # Prepare context
        context = super(CollectionViewTemplate, self).get_context_data()
        context["collection"] = collection
        context["collection_albums"] = collection.albums.all()
        context["collection_comments"] = collection_comments
        context["limit"] = _limit
        return context
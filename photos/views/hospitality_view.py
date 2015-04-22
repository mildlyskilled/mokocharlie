import logging
from django.views.generic import CreateView, FormView

from django.views.generic.base import TemplateView
from common.models import *
from moko.forms import HospitalityContactForm
from moko.mixins.ajax import AjaxResponseMixin


LOGGER = logging.getLogger(__name__)


class HospitalityTemplate(TemplateView):
    template_name = "hospitality/index.html"
    default_limit = 21
    default_page = 1
    default_order = 'recent'

    def get_context_data(self, **kwargs):
        hotels = Hospitality.objects.filter(published=1)
        # Get comments
        comments = Comment.objects.all().filter(comment_approved=1)[:8]
        # context
        context = super(HospitalityTemplate, self).get_context_data()
        context['hotels'] = hotels
        context["limit"] = self.default_limit
        context["comments"] = comments
        return context


class HospitalityViewTemplate(TemplateView):
    template_name = "hospitality/view.html"
    default_limit = 21
    default_page = 1

    def get_context_data(self, **kwargs):
        _limit = self.request.GET.get('limit', self.default_limit)
        _page = self.request.GET.get('page', self.default_page)
        hospitality_id = self.kwargs.get('hospitality_id')
        hospitality = Hospitality.objects.get(id=hospitality_id)

        # Get images for this hotel/resort
        albums = hospitality.albums.all()
        images = Photo.objects.filter(albums__in=albums)
        image_ids = [i.id for i in images]
        album_comments = Comment.objects.filter(image__albums__in=albums).filter(comment_approved=1).order_by(
            '-comment_date')

        context = super(HospitalityViewTemplate, self).get_context_data()
        context['hospitality'] = hospitality
        context['limit'] = _limit
        context['album_images'] = images
        context['album_comments'] = album_comments
        return context


class HospitalityContactTemplate(FormView):
    template_name = "partials/hospitality_contact_form.html"
    form_class = HospitalityContactForm

    def get(self, request, *args, **kwargs):
        return super(HospitalityContactTemplate, self).get(request, *args, **kwargs)
import logging

from django.views.generic.base import TemplateView
from common.models import *


LOGGER = logging.getLogger(__name__)


class HospitalityTemplate(TemplateView):
    template_name = "albums/index.html"
    default_limit = 21
    default_page = 1
    default_order = 'recent'

    def get_context_data(self, **kwargs):
        context = super(HospitalityTemplate, self).get_context_data()
        return context
import logging

from django.views.generic.base import TemplateView
from common.models import *


class ClassifiedsViewTemplate(TemplateView):

    template_name = 'classifieds/index.html'
    def get_context_data(self, **kwargs):
        context = super(ClassifiedsViewTemplate, self).get_context_data()

        return context
import logging

from django.views.generic.base import TemplateView
from classifieds.models import *


class ClassifiedsTemplate(TemplateView):
    template_name = 'classifieds/index.html'

    def get_context_data(self, **kwargs):
        context = super(ClassifiedsTemplate, self).get_context_data()
        jobs = Job.objects.filter(published=1)[:10]
        companies = Company.objects.filter(published=1)[:10]
        context['jobs'] = jobs
        context['companies'] = companies
        return context


class ClassifiedsTypeListTemplate(TemplateView):
    template_name = 'classifieds/index.html'


class ClassifiedsSingleViewTemplate(TemplateView):
    template_name = 'classifieds/view.html'
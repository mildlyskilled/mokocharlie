import logging
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from common.models import *


class ClassifiedsTemplate(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ClassifiedsTemplate, self).get_context_data()
        return context


class ClassifiedsTypeListTemplate(ListView):
    def get_context_data(self, **kwargs):
        context = super(ClassifiedsTypeListTemplate, self).get_context_data()
        return context


class ClassifiedsSingleViewTemplate(DetailView):
    def get_context_data(self, **kwargs):
        context = super(ClassifiedsSingleViewTemplate, self).get_context_data()
        return context
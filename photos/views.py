from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


class PhotosTemplate(TemplateView):
    template_name = "photos/index.html"

    def get_context_data(self, **kwargs):
        context = super(PhotosTemplate, self).get_context_data()
        context["images"] = "A list of all photos"
        return context


class PhotoViewTemplate(TemplateView):
    template_name = "photos/view.html"

    def get_context_data(self, **kwargs):
        context = super(PhotoViewTemplate, self).get_context_data()
        context["image"] = self.kwargs.get('image_id')
        return context
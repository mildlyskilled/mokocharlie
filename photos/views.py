from django.views.generic.base import TemplateView
from photos.models import *


class PhotosTemplate(TemplateView):
    template_name = "photos/index.html"

    def get_context_data(self, **kwargs):
        images = Photo.objects.all()
        context = super(PhotosTemplate, self).get_context_data()
        context["images"] = images
        return context


class PhotoViewTemplate(TemplateView):
    template_name = "photos/view.html"

    def get_context_data(self, **kwargs):
        context = super(PhotoViewTemplate, self).get_context_data()
        context["image"] = Photo.objects.get(image_id=self.kwargs.get('image_id'))
        return context
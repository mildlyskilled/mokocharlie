from django.views.generic.base import TemplateView
from moko.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PhotosTemplate(TemplateView):
    template_name = "photos/index.html"
    default_limit = 24
    default_page = 1

    def get_context_data(self, **kwargs):
        images = Photo.objects.all().order_by('-created_at')
        _limit = self.request.GET.get('limit', self.default_limit)
        _page = self.request.GET.get('page', self.default_page)
        p = Paginator(images, _limit)
        try:
            image_list = p.page(_page)
        except PageNotAnInteger:
            image_list = p.page(self.default_page)
        except EmptyPage:
            image_list = p.page(p.num_pages)

        context = super(PhotosTemplate, self).get_context_data()
        context["images"] = image_list
        context["paginator_object"] = image_list
        return context


class PhotoViewTemplate(TemplateView):
    template_name = "photos/view.html"

    def get_context_data(self, **kwargs):
        context = super(PhotoViewTemplate, self).get_context_data()
        context["image"] = Photo.objects.get(id=self.kwargs.get('image_id'))
        context["recent_images"] = Photo.objects.all()[:8]
        return context
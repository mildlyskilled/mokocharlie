from django.views.generic.base import TemplateView
from moko.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
import logging
from moko.forms import CommentForm

LOGGER = logging.getLogger(__name__)


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
        return context


class PhotoViewTemplate(TemplateView):
    template_name = "photos/view.html"

    def get_context_data(self, **kwargs):
        context = super(PhotoViewTemplate, self).get_context_data()
        photo = Photo.objects.get(id=self.kwargs.get('image_id'))
        context["image"] = photo
        context['comments'] = photo.comment_set.filter(comment_approved=1)
        context["recent_images"] = Photo.objects.all()[:8]
        if self.request.method == 'POST':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                print form_data
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.comment_approved = request.user.is_authenticated()  # use authenticated value to set approval status
            c.image = Photo.objects.get(id=self.kwargs.get('image_id'))
            c.comment_reported = False
            c.comment_report_type = 0
            c.save()
            return HttpResponseRedirect(request.path)
        else:
            return HttpResponseRedirect(request.path)


class NewCommentViewTemplate(TemplateView):
    template_name = "partials/comment_form.html"

    def get_context_data(self, **kwargs):
        context = super(NewCommentViewTemplate, self).get_context_data()
        context["form"] = CommentForm
        from time import sleep
        sleep(3)
        return context
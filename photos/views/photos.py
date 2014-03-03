from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from moko.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
import logging
from moko.forms import CommentForm
from moko.mixins.ajax import AjaxResponseMixin

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
        image_id = self.kwargs.get('image_id')
        context = super(PhotoViewTemplate, self).get_context_data()
        photo = Photo.objects.get(id=image_id)

        album_photos = Photo.objects.filter(albums__photos__id__exact=image_id).order_by('created_at').all()

        # find current key to get next and previous images
        current = [p for p in album_photos].index(photo)

        next = 0
        if current < album_photos.count() - 1:
            next = current + 1

        previous = album_photos.count() - 1

        if current > 0:
            previous = current - 1


        context["image"] = photo
        context['comments'] = photo.comment_set.filter(comment_approved=1)
        context["recent_images"] = Photo.objects.all()[:8]

        context["total_photos"] = album_photos.count()
        context["next_image"] = album_photos[next]
        context["previous_image"] = album_photos[previous]
        context["current_image_number"] = current + 1

        if self.request.method == 'POST':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                print form_data
        return context


class NewCommentViewTemplate(AjaxResponseMixin, CreateView):
    template_name = "partials/comment_form.html"
    model = Comment
    form_class = CommentForm
    object = Comment

    def get_form_kwargs(self):
        author_name = None
        if self.request.user.is_authenticated():
            author_name = "{0} {1}".format(self.request.user.first_name, self.request.user.last_name)
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['initial'] = {'image': self.request.GET.get('image_id'), 'comment_author': author_name}
        return kwargs

    def get(self, request, *args, **kwargs):
        return super(NewCommentViewTemplate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.comment_approved = request.user.is_authenticated()  # use authenticated value to set approval status
            c.image = Photo.objects.get(id=request.POST.get('image'))
            c.comment_reported = False
            c.comment_report_type = 0
            c.save()
            if self.request.is_ajax():
                data = {
                    'image_id': request.POST.get('image'),
                }
                return self.render_to_json_response(data)
            else:
                return HttpResponseRedirect(request.path)
        else:
            return self.form_invalid(form)


class CommentListViewTemplate(TemplateView):
    template_name = "partials/comment_list.html"

    def get_context_data(self, **kwargs):


        if self.request.GET.get('image_id') is not None:
            #get comments on an image
            image_id = self.request.GET.get('image_id')
            image = Photo.objects.get(id=image_id)
            comments = image.comment_set.filter(comment_approved=1).order_by('-comment_date');
        elif self.request.GET.get('album_id') is not None:
            #get comments on all images in given album
            album_id = self.request.GET.get('album_id')
            comments = Comment.objects.filter(image__album=album_id).filter(comment_approved=1).order_by(
                '-comment_date')
        else:
            #get most recent comments
            comments = Comment.objects.all()[:10]

        context = super(CommentListViewTemplate, self).get_context_data()
        context['comments'] = comments
        return context
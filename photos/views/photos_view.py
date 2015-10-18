import json
import logging
from cloudinary.uploader import upload

from django.contrib import messages
from django.utils.timezone import now
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from ipware.ip import get_real_ip, get_ip
from moko.forms import CommentForm, PhotoUploadForm
from moko.mixins.ajax import AjaxResponseMixin
from common.models import *
from datetime import datetime
LOGGER = logging.getLogger(__name__)


def increment_views(request, kwargs):
    view_count = PhotoViews.objects.filter(photo_id=kwargs.get("image_id"))
    if request.user.is_authenticated:
        view_count.filter(user=request.user.id)
    else:
        view_count.filter(ip_address=get_real_ip(request))

    print len(view_count.all())
    if len(view_count.all()) == 0:
        pv = PhotoViews()
        pv.ip_address = get_ip(request)
        pv.photo_id = kwargs.get("image_id")
        if request.user.is_authenticated:
            pv.user = request.user
        pv.save()


class PhotosTemplate(TemplateView):
    template_name = "photos/index.html"
    default_limit = 40
    default_page = 1
    default_order = 'recent'

    def get_context_data(self, **kwargs):
        images = Photo.objects.filter(published=1).order_by('-created_at')
        _limit = self.request.GET.get('limit', self.default_limit)
        _order = self.request.GET.get('order', self.default_order)
        from collections import OrderedDict

        _order_dict_unsorted = {
            'recent': ['-created_at', 'Most Recent'],
            'alpha': ['name', 'Alphabetical'],
            'popular': ['-times_viewed', 'Most Viewed'],
            'rating': ['-times_rated', 'Most Rated'],
            'mostcomments': ['-comment_count', 'Most Comments'],
        }

        if _order in _order_dict_unsorted:
            if _order == 'mostcomments':
                from django.db.models.aggregates import Sum
                images = Photo.objects.annotate(comment_count=Sum('comment')).order_by(
                    _order_dict_unsorted[_order][0]).all()
            elif _order == "popular":
                from django.db.models.aggregates import Count
                images = Photo.objects.annotate(times_viewed=Count('photoviews')).order_by(
                    _order_dict_unsorted[_order][0]).all()
            else:
                images = Photo.objects.distinct().order_by(_order_dict_unsorted[_order][0]).all()

        _order_dict = OrderedDict(sorted(_order_dict_unsorted.items()), key=lambda t: t[0], reverse=True)
        comments = Comment.objects.all().filter(comment_approved=1)[:12]
        context = super(PhotosTemplate, self).get_context_data()
        context['images'] = images
        context['limit'] = int(_limit)
        context['order'] = {'selected': _order, 'dictionary': _order_dict}
        context['comments'] = comments
        return context


class PhotoViewTemplate(TemplateView):
    template_name = "photos/view.html"

    def get_context_data(self, **kwargs):
        increment_views(self.request, kwargs)
        image_id = self.kwargs.get('image_id')
        context = super(PhotoViewTemplate, self).get_context_data()
        photo = Photo.objects.get(id=image_id)

        album_photos = Photo.objects.filter(albums__photo__id__exact=image_id).order_by('created_at').all()

        # find current key to get next and previous images
        current = [p for p in album_photos].index(photo)

        next_item = 0
        if current < album_photos.count() - 1:
            next_item = current + 1

        previous_item = album_photos.count() - 1

        if current > 0:
            previous_item = current - 1

        context["image"] = photo
        context['comments'] = photo.comment_set.filter(comment_approved=1)
        context["recent_images"] = Photo.objects.all()[:8]
        if self.request.user.is_authenticated():
            # get the favourite by user and image id
            context["favourited"] = Favourite.objects.filter(user_id=self.request.user.id).filter(photo_id=image_id)
        else:
            ip = get_real_ip(self.request) or get_ip(self.request)
            context["favourited"] = Favourite.objects.filter(client_ip=ip).filter(photo_id=image_id)

        context["total_photos"] = album_photos.count()
        context["next_image"] = album_photos[next_item]
        context["previous_image"] = album_photos[previous_item]
        context["current_image_number"] = current + 1
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
        kwargs['initial'] = {'image': self.request.GET.get('image_id'), 'comment_author': author_name,
                             'comment_date': now()}
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
            # get comments on an image
            image_id = self.request.GET.get('image_id')
            image = Photo.objects.get(id=image_id)
            comments = image.comment_set.filter(comment_approved=1).order_by('-comment_date');
        elif self.request.GET.get('album_id') is not None:
            # get comments on all images in given album
            album_id = self.request.GET.get('album_id')
            comments = Comment.objects.filter(image__album=album_id).filter(comment_approved=1).order_by(
                '-comment_date')
        else:
            # get most recent comments
            comments = Comment.objects.all()[:10]

        context = super(CommentListViewTemplate, self).get_context_data()
        context['comments'] = comments
        return context


class FavouritePhotoViewTemplate(AjaxResponseMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        ip = get_real_ip(request) or get_ip(request)
        image = kwargs['photo_id']
        data = {'status': 'failed'}

        f = Favourite.objects.filter(user_id=request.user.id).filter(photo_id=image)
        if f:
            data['message'] = 'You have already added this image to your favourites'
        else:
            try:
                f1 = Favourite(photo_id=image, client_ip=ip, user_id=request.user.id)
                f1.save()
                data = {'status': 'success', 'photo': image, 'ip': ip, 'user': request.user.id}
            except ValueError:
                data['message'] = "Could not add this photo to favourites"

        return self.render_to_json_response(json.dumps(data))


class UnFavouritePhotoViewTemplate(AjaxResponseMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        ip = get_real_ip(request) or get_ip(request)
        image = kwargs['photo_id']
        data = {'status': 'failed'}

        f = Favourite.objects.filter(user_id=request.user.id).filter(photo_id=image)
        if f:
            f.delete()
            data = {'status': 'success', 'photo': image, 'ip': ip, 'user': request.user.id}
        else:
            try:
                f = Favourite.objects.filter(photo_id=image, client_ip=ip)
                f.delete()
                data = {'status': 'success', 'photo': image, 'ip': ip}
            except ValueError:
                data['message'] = "Could not add this photo to favourites"

        return self.render_to_json_response(json.dumps(data))


class UploadPhotoTemplate(CreateView):
    template_name = "upload/index.html"
    model = Photo
    form_class = PhotoUploadForm
    object = Photo

    def get_form_kwargs(self):
        import uuid
        owner = self.request.user
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['initial'] = {'owner': owner, 'created_at': datetime.now(),
                             'updated_at': datetime.now(), 'image_id': uuid.uuid1()}

        return kwargs

    def get(self, request, *args, **kwargs):
        return super(UploadPhotoTemplate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            published = request.user.is_staff
            p.published = published
            cloudinary_data = upload(p.cloud_image)
            p.image_id = cloudinary_data['public_id']
            p.save()
            form.save_m2m()
            messages.add_message(self.request, messages.SUCCESS,
                                 'Successfully uploaded your image to the Mokocharlie Cloud')
        else:
            print form
            messages.add_message(self.request, messages.ERROR,
                                 'There was a problem uploading you photo')
            return self.form_invalid(form)

        return HttpResponseRedirect(reverse('upload_photos'))

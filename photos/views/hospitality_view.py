import logging
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, FormView

from django.views.generic.base import TemplateView
from common.models import *
from moko.forms import HospitalityContactForm
from django.conf import settings

LOGGER = logging.getLogger(__name__)


class HospitalityTemplate(TemplateView):
    template_name = "hospitality/index.html"
    default_limit = 21
    default_page = 1
    default_order = 'recent'

    def get_context_data(self, **kwargs):
        hotels = Hospitality.objects.filter(published=1)
        # Get comments
        comments = Comment.objects.all().filter(comment_approved=1)[:8]
        # context
        context = super(HospitalityTemplate, self).get_context_data()
        context['hotels'] = hotels
        context["limit"] = self.default_limit
        context["comments"] = comments
        return context


class HospitalityViewTemplate(TemplateView):
    template_name = "hospitality/view.html"
    default_limit = 21
    default_page = 1

    def get_context_data(self, **kwargs):
        _limit = self.request.GET.get('limit', self.default_limit)
        _page = self.request.GET.get('page', self.default_page)
        hospitality_id = self.kwargs.get('hospitality_id')
        hospitality = Hospitality.objects.get(id=hospitality_id)
        # Get images for this hotel/resort
        albums = hospitality.albums.all()
        images = Photo.objects.filter(albums__in=albums)
        image_ids = [i.id for i in images]
        album_comments = Comment.objects.filter(image__albums__in=albums).filter(comment_approved=1).order_by(
            '-comment_date')

        context = super(HospitalityViewTemplate, self).get_context_data()
        contact = self.request.GET.get('contact')
        if contact:
            context["contact"] = True
        context['hospitality'] = hospitality
        context['limit'] = _limit
        context['album_images'] = images
        context['album_comments'] = album_comments
        return context


class HospitalityContactTemplate(TemplateView):
    template_name = "hospitality/view.html"

    def get_context_data(self, **kwargs):
        hospitality_id = self.kwargs.get('hospitality_id')
        hospitality = Hospitality.objects.get(id=hospitality_id)
        context = super(HospitalityContactTemplate, self).get_context_data()
        context['hospitality'] = hospitality
        context["form"] = HospitalityContactForm()
        return context

    def post(self, request, *args, **kwargs):
        hospitality_id = kwargs.get("hospitality_id")
        form = HospitalityContactForm(request.POST)
        if form.is_valid():
            hospitality = Hospitality.objects.get(id=hospitality_id)
            sender_email = request.POST.get("email")
            sender_name = request.POST.get("name")
            sender_message = request.POST.get("message")

            # TODO use a template for this
            html_content = """Dear {0}, you got a message through mokocharlie <br />
                           From <strong>{1}<{2}></strong><br />
                           {3}<br />
                           Kind Regards,<br />
                           Mokocharlie
                          """.format(hospitality.contact.first_name, sender_name, sender_email, sender_message)

            content = """Dear {0}, you got a message through mokocharlie
                           From {1}<{2}>
                           {3}
                           Kind Regards,
                           Mokocharlie
                          """.format(hospitality.contact.first_name, sender_name, sender_email, sender_message)

            subject = 'Contact From Mokocharlie'

            try:

                email = EmailMultiAlternatives(subject, content, settings.ADMIN_EMAIL, [hospitality.contact.email])
                email.extra_headers['X-Mailgun-Tag'] = [hospitality.name]
                email.attach_alternative(html_content, "text/html")
                email.send()

                # send_mail(subject,
                #          content,
                #          settings.ADMIN_EMAIL,
                #          [hospitality.contact.email], html_message=html_content)
            except BadHeaderError:
                messages.add_message(self.request, messages.ERROR, 'Invalid header')

            messages.add_message(self.request, messages.SUCCESS, 'Your message has been sent')

        else:
            messages.add_message(self.request, messages.INFO, 'Please check your form input')

        return HttpResponseRedirect(reverse("hospitality_view", args=(hospitality_id,)))

import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.http import is_safe_url
from django.contrib.auth import logout
from django.shortcuts import redirect, resolve_url, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib import messages
from common.models import *
from moko.forms import LoginForm, ContactUsForm
from django.core.exceptions import ValidationError

LOGGER = logging.getLogger(__name__)


class HomeTemplateView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        recent_albums = Album.objects.filter(published=1).filter(featured=1)[:5]
        featured_collections = Collection.objects.filter(published=1).filter(featured=1)[:8]
        context = super(HomeTemplateView, self).get_context_data()
        context['featured_albums'] = recent_albums
        context['featured_collections'] = featured_collections
        return context


class LoginViewTemplate(FormView):
    form_class = LoginForm
    template_name = "profile/login.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            messages.add_message(self.request, messages.SUCCESS, 'You are already logged in')
            redirect_to = self.request.GET.get('next', '')
            if not is_safe_url(url=redirect_to, host=self.request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
                return redirect(redirect_to)

        return super(LoginViewTemplate, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        redirect_to = self.request.GET.get('next', '')
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        email = self.request.POST['email']
        password = self.request.POST['password']
        user = authenticate(email=email, password=password)
        if user:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, 'Successfully logged in')
        else:
            messages.add_message(self.request, messages.WARNING, 'Could not log you in')
            return redirect('login')

        return redirect(redirect_to)


class LogoutViewTemplate(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(self.request, messages.SUCCESS, 'You have been logged out')
        redirect_to = self.request.GET.get('next', '')
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        return redirect(redirect_to)


class ContactViewTemplate(FormView):
    form_class = ContactUsForm
    template_name = "home/contact.html"

    def get(self, request, *args, **kwargs):
        return super(ContactViewTemplate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = ContactUsForm(request.POST or None)
        context = {"form": form}

        if form.is_valid():
            sender_email = request.POST.get("email")
            sender_name = request.POST.get("name")
            sender_message = request.POST.get("message")

            # TODO use a template for this
            html_content = """Dear {0}, you got a message through the website <br />
                           From <strong>{1}<{2}></strong><br />
                           {3}<br />
                           Kind Regards,<br />
                           Mokocharlie
                          """.format("Mokocharlie Team", sender_name, sender_email, sender_message)

            content = """Dear {0}, you got a message through the website
                           From {1}<{2}>
                           {3}
                           Kind Regards,
                           Mokocharlie
                          """.format("Mokocharlie Team", sender_name, sender_email, sender_message)

            subject = 'Contact From Mokocharlie'

            try:

                email = EmailMultiAlternatives(subject, content, sender_email, [settings.ADMIN_EMAIL])
                email.extra_headers['X-Mailgun-Tag'] = ["web contact"]
                email.attach_alternative(html_content, "text/html")
                email.send()
            except BadHeaderError:
                messages.add_message(request, messages.ERROR, 'Invalid header', extra_tags={"DANGER": "danger"})
                return render_to_response(self.template_name, context=context, context_instance=RequestContext(request))
            except ValidationError:
                messages.add_message(request, messages.ERROR, 'Please check your form input',
                                     extra_tags={"DANGER": "danger"})
                return render_to_response(self.template_name,  context=context, context_instance=RequestContext(request))

            messages.add_message(request, messages.SUCCESS, 'Your message has been sent')

        else:
            messages.add_message(request, messages.INFO, 'Please check your form input')
            return render_to_response(self.template_name, context=context, context_instance=RequestContext(request))

        LOGGER.info("Email sent to {0} from {1}".format(settings.ADMIN_EMAIL, sender_email))
        return HttpResponseRedirect(reverse("home"))

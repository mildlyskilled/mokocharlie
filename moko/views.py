from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.http import is_safe_url
from django.contrib.auth import logout
from django.shortcuts import redirect, resolve_url
from django.contrib.auth import authenticate, login
from django.contrib import messages
from common.models import *
from datetime import datetime
from django.utils.timezone import utc
from moko.forms import LoginForm

class HomeViewTemplate(TemplateView):
    template_name = "home/index.html"
    def get_context_data(self, **kwargs):
        recent_albums = Album.objects.filter(published=1).filter(featured=1)[:5]
        featured_collections = Collections.objects.filter(published=1).filter(featured=1)[:6]
        classifieds = Classified.objects.filter(published=1).filter(published_date__lte=datetime.utcnow().replace(tzinfo=utc))
        context = super(HomeViewTemplate, self).get_context_data()
        context["home"] = "El Homie"
        context['featured_albums'] = recent_albums
        context['featured_collections'] = featured_collections
        context['classifieds'] = classifieds
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
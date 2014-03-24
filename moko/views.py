from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.http import is_safe_url
from django.contrib.auth import logout
from django.shortcuts import redirect, resolve_url
from django.contrib.auth import authenticate, login

from moko.forms import LoginForm


class HomeViewTemplate(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeViewTemplate, self).get_context_data()
        context["home"] = "El Homie"
        return context


class LoginViewTemplate(FormView):
    form_class = LoginForm
    template_name = "profile/login.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
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
        login(self.request, user)
        return redirect(redirect_to)


class LogoutViewTemplate(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        redirect_to = self.request.GET.get('next', '')
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        return redirect(redirect_to)
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

class ProfileViewTemplate(TemplateView):
    """ Provides a simple view containing a users' profile details """
    model = User  #FIX ME use a richer profile model
    template_name = "profile/view.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('next'):
            return redirect(self.request.GET.get('next'))
        else:
            return super(ProfileViewTemplate, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user
from common.models import MokoUser
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from common.models import Comment


class ProfileViewTemplate(TemplateView):
    """ Provides a simple view containing a users' profile details """
    model = MokoUser
    template_name = "profile/view.html"
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('next'):
            return redirect(self.request.GET.get('next'))
        else:
            return super(ProfileViewTemplate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated():
            user = self.request.user
            context = super(ProfileViewTemplate, self).get_context_data()
            photo_comments = Comment.objects.filter(image__owner=user.id)
            context['photo_comments'] = photo_comments
            return context

    def get_object(self, queryset=None):
        return self.request.user
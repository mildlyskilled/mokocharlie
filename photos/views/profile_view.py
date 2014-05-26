from common.models import MokoUser, Comment, Classified, Contact
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from moko.forms import CustomUserCreationForm, ClassifiedForm, CustomUserChangeForm
from django.views.generic.edit import FormView, FormMixin
import datetime


class ProfileViewTemplate(FormMixin, DetailView):
    """ Provides a simple view containing a users' profile details """
    model = MokoUser
    template_name = "profile/view.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('next'):
            return redirect(self.request.GET.get('next'))
        else:
            return super(ProfileViewTemplate, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated():
            user = self.request.user
            edit_tab = self.request.GET.get('state')
            context = super(ProfileViewTemplate, self).get_context_data()
            photo_comments = Comment.objects.filter(image__owner=user.id)
            classifieds = Classified.objects.filter(owner=user)
            context['photo_comments'] = photo_comments
            context['classifieds'] = classifieds
            context['today'] = datetime.datetime.now()
            classified_form_object = ClassifiedForm(instance=Classified())
            classified_form_object.fields['owner'].queryset = Contact.objects.filter(owner=self.request.user)
            context['classified_form'] = classified_form_object
            if edit_tab is not None:
                context['edit_form'] = CustomUserChangeForm(instance=self.request.user)

            return context

    def get_object(self, queryset=None):
        return self.request.user


class ExtraDetailsViewTemplate(FormView):
    """ Some social login providers don't offer all the details we require
    for a full user registration (email addresses etc.).

    This view prompts the user for any extra fields we'd like them to complete
    before completing registration.

    Can currently only be used as part of the python_social_auth pipeline.

    """
    form_class = CustomUserCreationForm
    template_name = "profile/create_account.html"
    success_url = "/profile/"

    def get_initial(self):
        if 'partial_pipeline' in self.request.session:
            return self.request.session['partial_pipeline']['kwargs']['details']
        else:
            return {}

    def form_valid(self, form):
        for key, value in form.cleaned_data.iteritems():
            self.request.session[key] = value
        # This is the somewhat magic stuff that python_social_auth requires
        # to continue a social login after submission.
        if 'partial_pipeline' in self.request.session:
            backend = self.request.session['partial_pipeline']['backend']
        else:
            backend = "email"
        return redirect('social:complete', backend=backend)
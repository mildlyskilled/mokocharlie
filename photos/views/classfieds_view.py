import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from common.models import *
from django.views.generic.edit import CreateView
from moko.forms import ClassifiedForm


class ClassifiedsTemplate(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ClassifiedsTemplate, self).get_context_data()
        return context


class ClassifiedsTypeListTemplate(ListView):
    def get_context_data(self, **kwargs):
        context = super(ClassifiedsTypeListTemplate, self).get_context_data()
        return context


class ClassifiedsSingleViewTemplate(DetailView):
    def get_context_data(self, **kwargs):
        context = super(ClassifiedsSingleViewTemplate, self).get_context_data()
        return context


class NewClassifiedsTemplate(CreateView):
    """ Create new classifieds item but users need to be logged in first """
    template_name = "classifieds/new.html"
    form_class = ClassifiedForm
    object = Classified
    model = Classified

    def get_form_kwargs(self):
        now = datetime.datetime.now()
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['initial'] = {'owner': self.request.user.id, 'created_at': now, 'updated_at': now,
                             'published': self.request.user.is_staff}
        return kwargs

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('next'):
            return redirect(self.request.GET.get('next'))
        else:
            return super(NewClassifiedsTemplate, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = ClassifiedForm(request.POST)
        print request.POST
        if form.is_valid():
            c = form.save(commit=False)
            # zip the meta data key values into one dict
            meta_unclean = dict(zip(request.POST.getlist('key[]'), request.POST.getlist('value[]')))
            c.meta_data = json.dumps(meta_unclean)
            c.save()

            return HttpResponseRedirect(request.path)
        else:
            return self.form_invalid(form)

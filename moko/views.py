from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, RedirectView
from django.http import HttpResponse

def home(request):
    content = "El home"
    return HttpResponse(content)

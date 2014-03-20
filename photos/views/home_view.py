from django.views.generic.base import TemplateView


class HomeViewTemplate(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeViewTemplate, self).get_context_data()
        context["home"] = "El Homie"
        return context

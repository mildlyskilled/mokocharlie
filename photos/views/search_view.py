from haystack.views import SearchView
from moko.forms import GeneralSearchForm


class SearchViewTemplate(SearchView):
    form_class = GeneralSearchForm

    def extra_context(self):
        extra = super(SearchViewTemplate, self).extra_context()

        if not self.results:
            extra['facets'] = self.form.search().facet_counts()
        else:
            extra['facets'] = self.results.facet_counts()

        return extra

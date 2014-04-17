import datetime
from haystack import indexes
from models import (Photo, Comment, Album)


class PhotoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='owner')
    pub_date = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return Photo

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())
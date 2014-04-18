import datetime
from haystack import indexes
from models import (Photo, Comment, Album)


class PhotoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='owner')
    pub_date = indexes.DateTimeField(model_attr='created_at')
    content_auto = indexes.EdgeNgramField(model_attr="name")

    def get_model(self):
        return Photo

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now()).filter(published=1)


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='created_at')
    content_auto = indexes.EdgeNgramField(model_attr="label")

    def get_model(self):
        return Album

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now()).filter(published=1)


class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    comment = indexes.CharField(model_attr="image_comment")
    author = indexes.CharField(model_attr="comment_author")
    pub_date = indexes.DateTimeField(model_attr="comment_date")

    def get_model(self):
        return Comment

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(comment_date__lte=datetime.datetime.now()).filter(
            comment_approved=1).filter(comment_reported=0)

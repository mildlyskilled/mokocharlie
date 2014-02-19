# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    image_id = models.CharField(max_length=20)
    name = models.CharField(max_length=250)
    path = models.CharField(max_length=150)
    caption = models.TextField()
    video = models.CharField(max_length=15, blank=True)
    times_viewed = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    owner = models.CharField(max_length=41)
    total_rating = models.BigIntegerField()
    times_rated = models.IntegerField()
    published = models.IntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'photo'
        ordering = '-created_at'

    def __unicode__(self):
        return self.name


class Album(models.Model):
    id = models.IntegerField(primary_key=True)
    album_id = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    cover = models.ForeignKey(Photo, db_column='id')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    published = models.IntegerField()
    photos = models.ManyToManyField(Photo, through='PhotoAlbum')

    class Meta:
        db_table = 'album'

    def __unicode__(self):
        return self.label

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('album_view', args=[str(self.id)])


class AppData(models.Model):
    id = models.IntegerField(primary_key=True)
    app_name = models.TextField()
    app_description = models.TextField()
    app_key = models.TextField()
    date_created = models.DateTimeField()
    created_by = models.CharField(max_length=41)
    enabled = models.IntegerField(blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)
    deleted_by = models.CharField(max_length=41, blank=True)
    deleted_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'app_data'


class AppProperties(models.Model):
    id = models.IntegerField(primary_key=True)
    app = models.ForeignKey(AppData)
    definition = models.ForeignKey('AppPropertyDefinitions')
    property_data = models.TextField()

    class Meta:
        db_table = 'app_properties'


class AppPropertyDefinitions(models.Model):
    id = models.IntegerField(primary_key=True)
    prop_handle = models.CharField(max_length=150)
    prop_name = models.CharField(max_length=250)
    prop_type = models.CharField(max_length=150)
    prop_required = models.IntegerField()
    prop_protected = models.IntegerField()

    class Meta:
        db_table = 'app_property_definitions'


class CloudinaryData(models.Model):
    id = models.IntegerField(primary_key=True)
    cloudinary_data = models.TextField(blank=True)
    associated_image = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'cloudinary_data'


class Hospitality(models.Model):
    id = models.IntegerField(primary_key=True)
    featured = models.IntegerField()
    hospitality_type = models.CharField(max_length=20)
    name = models.TextField()
    description = models.TextField()
    address = models.TextField()
    telephone = models.TextField()
    website = models.TextField()
    date_added = models.DateTimeField()
    published = models.IntegerField()

    class Meta:
        db_table = 'hospitality'

    def __unicode__(self):
        return self.name


class HospitalityAlbumLookup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    hospitality = models.ForeignKey(Hospitality)
    album = models.ForeignKey(Album)

    class Meta:
        db_table = 'hospitality_album_lookup'


class ImageComments(models.Model):
    comment_id = models.BigIntegerField(primary_key=True)
    image = models.ForeignKey('Photo')
    image_comment = models.TextField()
    comment_author = models.CharField(max_length=150)
    comment_date = models.DateTimeField()
    comment_approved = models.IntegerField()
    comment_reported = models.IntegerField()
    comment_report_type = models.IntegerField()
    report_comments = models.TextField(blank=True)

    class Meta:
        db_table = 'image_comments'

    def __unicode__(self):
        return self.image_comment


class PhotoAlbum(models.Model):
    id = models.IntegerField(primary_key=True)
    photo = models.ForeignKey(Photo)
    album = models.ForeignKey(Album)

    class Meta:
        managed = False
        db_table = 'photo_album'


class PhotoStories(models.Model):
    story_id = models.IntegerField(primary_key=True)
    story_name = models.CharField(max_length=150)
    story_description = models.TextField()
    story_album = models.ForeignKey(Album, db_column='story_album')
    date_added = models.DateTimeField()
    published = models.IntegerField()

    class Meta:
        db_table = 'photo_stories'


class Promotions(models.Model):
    promo_id = models.IntegerField(primary_key=True)
    promo_handle = models.CharField(max_length=50, blank=True)
    promo_type = models.CharField(max_length=20)
    promo_name = models.CharField(max_length=150)
    promo_instructions = models.TextField()
    promo_album = models.IntegerField(blank=True, null=True)
    static_image_path = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    featured = models.IntegerField()
    published = models.IntegerField()

    class Meta:
        db_table = 'promotions'


class SearchData(models.Model):
    search_id = models.CharField(primary_key=True, max_length=15)
    keywords = models.TextField()
    searcher_ip_address = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'search_data'


class UserImageLibrary(models.Model):
    id = models.IntegerField(primary_key=True)
    image_id = models.CharField(max_length=15)
    image_name = models.CharField(max_length=250)
    image_path = models.CharField(max_length=150)
    image_album = models.CharField(max_length=150)
    image_caption = models.TextField()
    image_source = models.CharField(max_length=11)
    times_viewed = models.IntegerField()
    date_added = models.DateTimeField()
    image_uploader = models.CharField(max_length=150)
    uploader_email = models.CharField(max_length=150)
    total_rating = models.BigIntegerField()
    times_rated = models.IntegerField()
    published = models.IntegerField()

    class Meta:
        db_table = 'user_image_library'


class VideoLibrary(models.Model):
    video_id = models.IntegerField(primary_key=True)
    external_id = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 'video_library'


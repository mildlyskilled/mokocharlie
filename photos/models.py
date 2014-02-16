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
    image_id = models.CharField(primary_key=True, max_length=20)
    image_name = models.CharField(max_length=250)
    image_path = models.CharField(max_length=150)
    image_album = models.CharField(max_length=150)
    image_caption = models.TextField()
    image_video = models.CharField(max_length=15, blank=True)
    times_viewed = models.IntegerField()
    date_added = models.DateTimeField()
    added_by = models.CharField(max_length=41)
    total_rating = models.BigIntegerField()
    times_rated = models.IntegerField()
    published = models.IntegerField()
    deleted = models.IntegerField()
    date_deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'image_library'

    def __unicode__(self):
        return u'%s' % self.image_name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('image_view', args=[str(self.image_id)])


class ReportedImage(models.Model):
    report_id = models.IntegerField(primary_key=True)
    image_id = models.CharField(max_length=15)
    reporter_name = models.CharField(max_length=150)
    reporter_email = models.CharField(max_length=150)
    reason = models.TextField()
    date_reported = models.DateTimeField()

    class Meta:
        db_table = 'reported_images'

    def __unicode__(self):
        return self.reason


class UserImage(models.Model):
    image_id = models.CharField(primary_key=True, max_length=15)
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

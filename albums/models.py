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


class Album(models.Model):
    album_id = models.IntegerField(primary_key=True)
    album_label = models.CharField(max_length=150)
    album_description = models.TextField()
    album_cover = models.CharField(max_length=15, blank=True)
    date_added = models.DateTimeField()
    published = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'album_data'

    def __unicode__(self):
        return u'%s' % self.album_label

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('album_view', args=[str(self.album_id)])
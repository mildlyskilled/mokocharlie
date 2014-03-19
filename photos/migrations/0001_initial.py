# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Album'
        db.create_table(u'album', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('album_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cover', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'cover_photo', null=True, to=orm['photos.Photo'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('published', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'photos', ['Album'])

        # Adding model 'Photo'
        db.create_table(u'photo', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('image_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('caption', self.gf('django.db.models.fields.TextField')()),
            ('video', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('times_viewed', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=41)),
            ('total_rating', self.gf('django.db.models.fields.BigIntegerField')()),
            ('times_rated', self.gf('django.db.models.fields.IntegerField')()),
            ('published', self.gf('django.db.models.fields.IntegerField')()),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'photos', ['Photo'])

        # Adding model 'AppData'
        db.create_table(u'app_data', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('app_name', self.gf('django.db.models.fields.TextField')()),
            ('app_description', self.gf('django.db.models.fields.TextField')()),
            ('app_key', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_by', self.gf('django.db.models.fields.CharField')(max_length=41)),
            ('enabled', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('deleted_by', self.gf('django.db.models.fields.CharField')(max_length=41, blank=True)),
            ('deleted_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'photos', ['AppData'])

        # Adding model 'AppProperties'
        db.create_table(u'app_properties', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.AppData'])),
            ('definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.AppPropertyDefinitions'])),
            ('property_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'photos', ['AppProperties'])

        # Adding model 'AppPropertyDefinitions'
        db.create_table(u'app_property_definitions', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('prop_handle', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('prop_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('prop_type', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('prop_required', self.gf('django.db.models.fields.IntegerField')()),
            ('prop_protected', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'photos', ['AppPropertyDefinitions'])

        # Adding model 'Hotel'
        db.create_table(u'hospitality', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('featured', self.gf('django.db.models.fields.IntegerField')()),
            ('hospitality_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('telephone', self.gf('django.db.models.fields.TextField')()),
            ('website', self.gf('django.db.models.fields.TextField')()),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')()),
            ('published', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'photos', ['Hotel'])

        # Adding model 'HospitalityAlbumLookup'
        db.create_table(u'hospitality_album_lookup', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('hospitality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Hotel'])),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Album'])),
        ))
        db.send_create_signal(u'photos', ['HospitalityAlbumLookup'])

        # Adding model 'Comment'
        db.create_table(u'image_comments', (
            ('comment_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Photo'])),
            ('image_comment', self.gf('django.db.models.fields.TextField')()),
            ('comment_author', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('comment_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('comment_approved', self.gf('django.db.models.fields.IntegerField')()),
            ('comment_reported', self.gf('django.db.models.fields.IntegerField')()),
            ('comment_report_type', self.gf('django.db.models.fields.IntegerField')()),
            ('report_comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'photos', ['Comment'])

        # Adding model 'PhotoStory'
        db.create_table(u'photo_stories', (
            ('story_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('story_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('story_description', self.gf('django.db.models.fields.TextField')()),
            ('story_album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Album'], db_column=u'story_album')),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')()),
            ('published', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'photos', ['PhotoStory'])

        # Adding model 'Promotion'
        db.create_table(u'promotions', (
            ('promo_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('promo_handle', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('promo_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('promo_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('promo_instructions', self.gf('django.db.models.fields.TextField')()),
            ('promo_album', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('static_image_path', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('featured', self.gf('django.db.models.fields.IntegerField')()),
            ('published', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'photos', ['Promotion'])

        # Adding model 'UserPhoto'
        db.create_table(u'user_image_library', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('image_id', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('image_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('image_path', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('image_album', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('image_caption', self.gf('django.db.models.fields.TextField')()),
            ('image_source', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('times_viewed', self.gf('django.db.models.fields.IntegerField')()),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')()),
            ('image_uploader', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('uploader_email', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('total_rating', self.gf('django.db.models.fields.BigIntegerField')()),
            ('times_rated', self.gf('django.db.models.fields.IntegerField')()),
            ('published', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'photos', ['UserPhoto'])

        # Adding model 'VideoLibrary'
        db.create_table(u'video_library', (
            ('video_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal(u'photos', ['VideoLibrary'])


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table(u'album')

        # Deleting model 'Photo'
        db.delete_table(u'photo')

        # Deleting model 'AppData'
        db.delete_table(u'app_data')

        # Deleting model 'AppProperties'
        db.delete_table(u'app_properties')

        # Deleting model 'AppPropertyDefinitions'
        db.delete_table(u'app_property_definitions')

        # Deleting model 'Hotel'
        db.delete_table(u'hospitality')

        # Deleting model 'HospitalityAlbumLookup'
        db.delete_table(u'hospitality_album_lookup')

        # Deleting model 'Comment'
        db.delete_table(u'image_comments')

        # Deleting model 'PhotoStory'
        db.delete_table(u'photo_stories')

        # Deleting model 'Promotion'
        db.delete_table(u'promotions')

        # Deleting model 'UserPhoto'
        db.delete_table(u'user_image_library')

        # Deleting model 'VideoLibrary'
        db.delete_table(u'video_library')


    models = {
        u'photos.album': {
            'Meta': {'ordering': "(u'-created_at',)", 'object_name': 'Album', 'db_table': "u'album'"},
            'album_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cover_photo'", 'null': 'True', 'to': u"orm['photos.Photo']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['photos.Photo']", 'through': u"orm['photos.PhotoAlbum']", 'symmetrical': 'False'}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'photos.appdata': {
            'Meta': {'object_name': 'AppData', 'db_table': "u'app_data'"},
            'app_description': ('django.db.models.fields.TextField', [], {}),
            'app_key': ('django.db.models.fields.TextField', [], {}),
            'app_name': ('django.db.models.fields.TextField', [], {}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '41'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.CharField', [], {'max_length': '41', 'blank': 'True'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'photos.appproperties': {
            'Meta': {'object_name': 'AppProperties', 'db_table': "u'app_properties'"},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.AppData']"}),
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.AppPropertyDefinitions']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'property_data': ('django.db.models.fields.TextField', [], {})
        },
        u'photos.apppropertydefinitions': {
            'Meta': {'object_name': 'AppPropertyDefinitions', 'db_table': "u'app_property_definitions'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'prop_handle': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'prop_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'prop_protected': ('django.db.models.fields.IntegerField', [], {}),
            'prop_required': ('django.db.models.fields.IntegerField', [], {}),
            'prop_type': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'photos.comment': {
            'Meta': {'ordering': "(u'-comment_date',)", 'object_name': 'Comment', 'db_table': "u'image_comments'"},
            'comment_approved': ('django.db.models.fields.IntegerField', [], {}),
            'comment_author': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'comment_date': ('django.db.models.fields.DateTimeField', [], {}),
            'comment_id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'comment_report_type': ('django.db.models.fields.IntegerField', [], {}),
            'comment_reported': ('django.db.models.fields.IntegerField', [], {}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Photo']"}),
            'image_comment': ('django.db.models.fields.TextField', [], {}),
            'report_comments': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'photos.hospitalityalbumlookup': {
            'Meta': {'object_name': 'HospitalityAlbumLookup', 'db_table': "u'hospitality_album_lookup'"},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Album']"}),
            'hospitality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Hotel']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'})
        },
        u'photos.hotel': {
            'Meta': {'object_name': 'Hotel', 'db_table': "u'hospitality'"},
            'address': ('django.db.models.fields.TextField', [], {}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.IntegerField', [], {}),
            'hospitality_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'telephone': ('django.db.models.fields.TextField', [], {}),
            'website': ('django.db.models.fields.TextField', [], {})
        },
        u'photos.photo': {
            'Meta': {'ordering': "(u'-created_at',)", 'object_name': 'Photo', 'db_table': "u'photo'"},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'photo_albums'", 'symmetrical': 'False', 'through': u"orm['photos.PhotoAlbum']", 'to': u"orm['photos.Album']"}),
            'caption': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'image_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '41'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'times_rated': ('django.db.models.fields.IntegerField', [], {}),
            'times_viewed': ('django.db.models.fields.IntegerField', [], {}),
            'total_rating': ('django.db.models.fields.BigIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        u'photos.photoalbum': {
            'Meta': {'object_name': 'PhotoAlbum', 'db_table': "u'photo_album'", 'managed': 'False'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Album']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Photo']"})
        },
        u'photos.photostory': {
            'Meta': {'ordering': "(u'-date_added',)", 'object_name': 'PhotoStory', 'db_table': "u'photo_stories'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'story_album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photos.Album']", 'db_column': "u'story_album'"}),
            'story_description': ('django.db.models.fields.TextField', [], {}),
            'story_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'story_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'photos.promotion': {
            'Meta': {'object_name': 'Promotion', 'db_table': "u'promotions'"},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'featured': ('django.db.models.fields.IntegerField', [], {}),
            'promo_album': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'promo_handle': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'promo_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'promo_instructions': ('django.db.models.fields.TextField', [], {}),
            'promo_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'promo_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'static_image_path': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'photos.searchdata': {
            'Meta': {'object_name': 'SearchData', 'db_table': "u'search_data'", 'managed': 'False'},
            'keywords': ('django.db.models.fields.TextField', [], {}),
            'search_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True'}),
            'searcher_ip_address': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'photos.userphoto': {
            'Meta': {'object_name': 'UserPhoto', 'db_table': "u'user_image_library'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'image_album': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'image_caption': ('django.db.models.fields.TextField', [], {}),
            'image_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'image_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'image_path': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'image_source': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'image_uploader': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'times_rated': ('django.db.models.fields.IntegerField', [], {}),
            'times_viewed': ('django.db.models.fields.IntegerField', [], {}),
            'total_rating': ('django.db.models.fields.BigIntegerField', [], {}),
            'uploader_email': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'photos.videolibrary': {
            'Meta': {'object_name': 'VideoLibrary', 'db_table': "u'video_library'"},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'video_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['photos']
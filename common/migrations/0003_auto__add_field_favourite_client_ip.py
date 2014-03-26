# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Favourite.client_ip'
        db.add_column(u'favourite', 'client_ip',
                      self.gf('django.db.models.fields.CharField')(max_length=13, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Favourite.client_ip'
        db.delete_column(u'favourite', 'client_ip')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'common.album': {
            'Meta': {'ordering': "(u'-created_at',)", 'object_name': 'Album', 'db_table': "u'album'"},
            'album_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cover_photo'", 'null': 'True', 'to': u"orm['common.Photo']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Photo']", 'through': u"orm['common.PhotoAlbum']", 'symmetrical': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'common.comment': {
            'Meta': {'ordering': "(u'-comment_date',)", 'object_name': 'Comment', 'db_table': "u'image_comments'"},
            'comment_approved': ('django.db.models.fields.BooleanField', [], {}),
            'comment_author': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'comment_date': ('django.db.models.fields.DateTimeField', [], {}),
            'comment_id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'comment_report_type': ('django.db.models.fields.IntegerField', [], {}),
            'comment_reported': ('django.db.models.fields.BooleanField', [], {}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Photo']"}),
            'image_comment': ('django.db.models.fields.TextField', [], {}),
            'report_comments': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'common.favourite': {
            'Meta': {'object_name': 'Favourite', 'db_table': "u'favourite'"},
            'client_ip': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 26, 0, 0)'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Photo']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MokoUser']"})
        },
        u'common.hospitalityalbum': {
            'Meta': {'object_name': 'HospitalityAlbum', 'db_table': "u'hospitality_albums'"},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Album']"}),
            'hospitality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Hotel']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'})
        },
        u'common.hotel': {
            'Meta': {'object_name': 'Hotel', 'db_table': "u'hospitality'"},
            'address': ('django.db.models.fields.TextField', [], {}),
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'hotel_album'", 'db_column': "u'hospitality_id'", 'to': u"orm['common.Album']", 'through': u"orm['common.HospitalityAlbum']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {}),
            'hospitality_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'telephone': ('django.db.models.fields.TextField', [], {}),
            'website': ('django.db.models.fields.TextField', [], {})
        },
        u'common.mokouser': {
            'Meta': {'object_name': 'MokoUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'common.photo': {
            'Meta': {'ordering': "(u'-created_at',)", 'object_name': 'Photo', 'db_table': "u'photo'"},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'photo_albums'", 'symmetrical': 'False', 'through': u"orm['common.PhotoAlbum']", 'to': u"orm['common.Album']"}),
            'caption': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'image_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'photo_owner'", 'db_column': "u'owner'", 'to': u"orm['common.MokoUser']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'times_rated': ('django.db.models.fields.IntegerField', [], {}),
            'times_viewed': ('django.db.models.fields.IntegerField', [], {}),
            'total_rating': ('django.db.models.fields.BigIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        u'common.photoalbum': {
            'Meta': {'object_name': 'PhotoAlbum', 'db_table': "u'photo_album'", 'managed': 'False'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Album']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Photo']"})
        },
        u'common.photostory': {
            'Meta': {'ordering': "(u'-date_added',)", 'object_name': 'PhotoStory', 'db_table': "u'photo_stories'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'story_album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Album']", 'db_column': "u'story_album'"}),
            'story_description': ('django.db.models.fields.TextField', [], {}),
            'story_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'story_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'common.promotion': {
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
        u'common.searchdata': {
            'Meta': {'object_name': 'SearchData', 'db_table': "u'search_data'", 'managed': 'False'},
            'keywords': ('django.db.models.fields.TextField', [], {}),
            'search_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'primary_key': 'True'}),
            'searcher_ip_address': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'common.videolibrary': {
            'Meta': {'object_name': 'VideoLibrary', 'db_table': "u'video_library'"},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'video_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']
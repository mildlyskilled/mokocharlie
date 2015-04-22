# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field albums on 'Album'
        m2m_table_name = db.shorten_name(u'common_album_albums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm[u'common.album'], null=False)),
            ('hospitality', models.ForeignKey(orm[u'common.hospitality'], null=False))
        ))
        db.create_unique(m2m_table_name, ['album_id', 'hospitality_id'])


    def backwards(self, orm):
        # Removing M2M table for field albums on 'Album'
        db.delete_table(db.shorten_name(u'common_album_albums'))


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
            'Meta': {'ordering': "(u'-created_at',)", 'object_name': 'Album'},
            'album_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['common.Hospitality']", 'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cover_photo'", 'null': 'True', 'to': u"orm['common.Photo']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 22, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 22, 0, 0)', 'null': 'True'})
        },
        u'common.collection': {
            'Meta': {'object_name': 'Collection'},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Album']", 'symmetrical': 'False'}),
            'cover_album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'cover_album'", 'null': 'True', 'to': u"orm['common.Album']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 22, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u'Collection'", 'max_length': '25'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 22, 0, 0)'})
        },
        u'common.comment': {
            'Meta': {'ordering': "(u'-comment_date',)", 'object_name': 'Comment'},
            'comment_approved': ('django.db.models.fields.BooleanField', [], {}),
            'comment_author': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'comment_date': ('django.db.models.fields.DateTimeField', [], {}),
            'comment_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Photo']"}),
            'image_comment': ('django.db.models.fields.TextField', [], {})
        },
        u'common.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MokoUser']"}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'common.favourite': {
            'Meta': {'object_name': 'Favourite'},
            'client_ip': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 22, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Photo']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MokoUser']"})
        },
        u'common.hospitality': {
            'Meta': {'ordering': "[u'-featured', u'-date_added']", 'object_name': 'Hospitality'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Album']", 'symmetrical': 'False'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'default': "u'hotelinquiry@mokocharlie.com'", 'max_length': '75'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {}),
            'hospitality_type': ('django.db.models.fields.CharField', [], {'default': "u'HOTEL'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'Meta': {'ordering': "(u'-created_at',)", 'object_name': 'Photo'},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Album']", 'symmetrical': 'False'}),
            'caption': ('django.db.models.fields.TextField', [], {}),
            'cloud_image': ('cloudinary.models.CloudinaryField', [], {'max_length': '100', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 22, 0, 0)'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_id': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'photo_owner'", 'db_column': "u'owner'", 'to': u"orm['common.MokoUser']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'times_viewed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 22, 0, 0)'}),
            'video': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Video']", 'symmetrical': 'False'})
        },
        u'common.photostory': {
            'Meta': {'ordering': "(u'-created_at',)", 'object_name': 'PhotoStory'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Album']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 22, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'published': ('django.db.models.fields.BooleanField', [], {})
        },
        u'common.promotion': {
            'Meta': {'object_name': 'Promotion'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'featured': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'promo_album': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'promo_handle': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'promo_instructions': ('django.db.models.fields.TextField', [], {}),
            'promo_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'promo_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'static_image_path': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'common.video': {
            'Meta': {'object_name': 'Video'},
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'external_source': ('django.db.models.fields.CharField', [], {'default': "u'YOUTUBE'", 'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
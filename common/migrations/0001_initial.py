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
            ('cover', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'cover_photo', null=True, to=orm['common.Photo'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')()),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'common', ['Album'])

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
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'photo_owner', db_column=u'owner', to=orm['common.MokoUser'])),
            ('total_rating', self.gf('django.db.models.fields.BigIntegerField')()),
            ('times_rated', self.gf('django.db.models.fields.IntegerField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'common', ['Photo'])

        # Adding model 'Hotel'
        db.create_table(u'hospitality', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')()),
            ('hospitality_type', self.gf('django.db.models.fields.CharField')(default=u'HOTEL', max_length=20)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('telephone', self.gf('django.db.models.fields.TextField')()),
            ('website', self.gf('django.db.models.fields.TextField')()),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(default=u'hotelinquiry@mokocharlie.com', max_length=75)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'common', ['Hotel'])

        # Adding model 'HospitalityAlbum'
        db.create_table(u'hospitality_album', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('hospitality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Hotel'])),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Album'])),
        ))
        db.send_create_signal(u'common', ['HospitalityAlbum'])

        # Adding model 'Comment'
        db.create_table(u'image_comments', (
            ('comment_id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Photo'])),
            ('image_comment', self.gf('django.db.models.fields.TextField')()),
            ('comment_author', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('comment_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('comment_approved', self.gf('django.db.models.fields.BooleanField')()),
            ('comment_reported', self.gf('django.db.models.fields.BooleanField')()),
            ('comment_report_type', self.gf('django.db.models.fields.IntegerField')()),
            ('report_comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'common', ['Comment'])

        # Adding model 'PhotoStory'
        db.create_table(u'photo_stories', (
            ('story_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('story_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('story_description', self.gf('django.db.models.fields.TextField')()),
            ('story_album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Album'], db_column=u'story_album')),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'common', ['PhotoStory'])

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
        db.send_create_signal(u'common', ['Promotion'])

        # Adding model 'VideoLibrary'
        db.create_table(u'video_library', (
            ('video_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal(u'common', ['VideoLibrary'])

        # Adding model 'MokoUser'
        db.create_table(u'common_mokouser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=254)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'common', ['MokoUser'])

        # Adding M2M table for field groups on 'MokoUser'
        m2m_table_name = db.shorten_name(u'common_mokouser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mokouser', models.ForeignKey(orm[u'common.mokouser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mokouser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'MokoUser'
        m2m_table_name = db.shorten_name(u'common_mokouser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mokouser', models.ForeignKey(orm[u'common.mokouser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mokouser_id', 'permission_id'])

        # Adding model 'Favourite'
        db.create_table(u'favourite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Photo'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.MokoUser'])),
            ('client_ip', self.gf('django.db.models.fields.CharField')(max_length=13, null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 26, 0, 0))),
        ))
        db.send_create_signal(u'common', ['Favourite'])

        # Adding model 'Collections'
        db.create_table(u'collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'Collection', max_length=25)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 26, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 26, 0, 0))),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('cover_album', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'cover_album', null=True, to=orm['common.Album'])),
        ))
        db.send_create_signal(u'common', ['Collections'])

        # Adding M2M table for field albums on 'Collections'
        m2m_table_name = db.shorten_name(u'collection_albums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collections', models.ForeignKey(orm[u'common.collections'], null=False)),
            ('album', models.ForeignKey(orm[u'common.album'], null=False))
        ))
        db.create_unique(m2m_table_name, ['collections_id', 'album_id'])

        # Adding model 'ClassifiedType'
        db.create_table(u'common_classifiedtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'common', ['ClassifiedType'])

        # Adding model 'Classified'
        db.create_table(u'common_classified', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 26, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 26, 0, 0))),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('unpublish_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.MokoUser'])),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
        ))
        db.send_create_signal(u'common', ['Classified'])

        # Adding M2M table for field types on 'Classified'
        m2m_table_name = db.shorten_name(u'common_classified_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('classified', models.ForeignKey(orm[u'common.classified'], null=False)),
            ('classifiedtype', models.ForeignKey(orm[u'common.classifiedtype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['classified_id', 'classifiedtype_id'])


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table(u'album')

        # Deleting model 'Photo'
        db.delete_table(u'photo')

        # Deleting model 'Hotel'
        db.delete_table(u'hospitality')

        # Deleting model 'HospitalityAlbum'
        db.delete_table(u'hospitality_album')

        # Deleting model 'Comment'
        db.delete_table(u'image_comments')

        # Deleting model 'PhotoStory'
        db.delete_table(u'photo_stories')

        # Deleting model 'Promotion'
        db.delete_table(u'promotions')

        # Deleting model 'VideoLibrary'
        db.delete_table(u'video_library')

        # Deleting model 'MokoUser'
        db.delete_table(u'common_mokouser')

        # Removing M2M table for field groups on 'MokoUser'
        db.delete_table(db.shorten_name(u'common_mokouser_groups'))

        # Removing M2M table for field user_permissions on 'MokoUser'
        db.delete_table(db.shorten_name(u'common_mokouser_user_permissions'))

        # Deleting model 'Favourite'
        db.delete_table(u'favourite')

        # Deleting model 'Collections'
        db.delete_table(u'collection')

        # Removing M2M table for field albums on 'Collections'
        db.delete_table(db.shorten_name(u'collection_albums'))

        # Deleting model 'ClassifiedType'
        db.delete_table(u'common_classifiedtype')

        # Deleting model 'Classified'
        db.delete_table(u'common_classified')

        # Removing M2M table for field types on 'Classified'
        db.delete_table(db.shorten_name(u'common_classified_types'))


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
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Photo']", 'through': u"orm['common.PhotoAlbum']", 'symmetrical': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'common.classified': {
            'Meta': {'object_name': 'Classified'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 26, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MokoUser']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.ClassifiedType']", 'symmetrical': 'False'}),
            'unpublish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 26, 0, 0)'})
        },
        u'common.classifiedtype': {
            'Meta': {'object_name': 'ClassifiedType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'common.collections': {
            'Meta': {'object_name': 'Collections', 'db_table': "u'collection'"},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Album']", 'symmetrical': 'False'}),
            'cover_album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'cover_album'", 'null': 'True', 'to': u"orm['common.Album']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 26, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u'Collection'", 'max_length': '25'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 26, 0, 0)'})
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 26, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Photo']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MokoUser']"})
        },
        u'common.hospitalityalbum': {
            'Meta': {'object_name': 'HospitalityAlbum', 'db_table': "u'hospitality_album'"},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Album']"}),
            'hospitality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Hotel']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'})
        },
        u'common.hotel': {
            'Meta': {'ordering': "[u'-featured', u'-date_added']", 'object_name': 'Hotel', 'db_table': "u'hospitality'"},
            'address': ('django.db.models.fields.TextField', [], {}),
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'hotel_album'", 'symmetrical': 'False', 'through': u"orm['common.HospitalityAlbum']", 'to': u"orm['common.Album']"}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'default': "u'hotelinquiry@mokocharlie.com'", 'max_length': '75'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {}),
            'hospitality_type': ('django.db.models.fields.CharField', [], {'default': "u'HOTEL'", 'max_length': '20'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
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
            'published': ('django.db.models.fields.BooleanField', [], {}),
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
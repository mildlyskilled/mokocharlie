# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Album'
        db.create_table(u'common_album', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cover', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'cover_photo', null=True, to=orm['common.Photo'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 27, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 27, 0, 0), null=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'common', ['Album'])

        # Adding model 'Photo'
        db.create_table(u'common_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_id', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')()),
            ('times_viewed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 27, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 27, 0, 0))),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'photo_owner', db_column=u'owner', to=orm['common.MokoUser'])),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('cloud_image', self.gf('cloudinary.models.CloudinaryField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'common', ['Photo'])

        # Adding M2M table for field video on 'Photo'
        m2m_table_name = db.shorten_name(u'common_photo_video')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm[u'common.photo'], null=False)),
            ('video', models.ForeignKey(orm[u'common.video'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photo_id', 'video_id'])

        # Adding M2M table for field albums on 'Photo'
        m2m_table_name = db.shorten_name(u'common_photo_albums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm[u'common.photo'], null=False)),
            ('album', models.ForeignKey(orm[u'common.album'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photo_id', 'album_id'])

        # Adding model 'Hospitality'
        db.create_table(u'common_hospitality', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        db.send_create_signal(u'common', ['Hospitality'])

        # Adding M2M table for field albums on 'Hospitality'
        m2m_table_name = db.shorten_name(u'common_hospitality_albums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hospitality', models.ForeignKey(orm[u'common.hospitality'], null=False)),
            ('album', models.ForeignKey(orm[u'common.album'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hospitality_id', 'album_id'])

        # Adding model 'Comment'
        db.create_table(u'common_comment', (
            ('comment_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Photo'])),
            ('image_comment', self.gf('django.db.models.fields.TextField')()),
            ('comment_author', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('comment_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('comment_approved', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'common', ['Comment'])

        # Adding model 'PhotoStory'
        db.create_table(u'common_photostory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Album'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 27, 0, 0))),
            ('published', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'common', ['PhotoStory'])

        # Adding model 'Promotion'
        db.create_table(u'common_promotion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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

        # Adding model 'Video'
        db.create_table(u'common_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('external_source', self.gf('django.db.models.fields.CharField')(default=u'YOUTUBE', max_length=25)),
        ))
        db.send_create_signal(u'common', ['Video'])

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
        db.create_table(u'common_favourite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Photo'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.MokoUser'])),
            ('client_ip', self.gf('django.db.models.fields.CharField')(max_length=13, null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 27, 0, 0))),
        ))
        db.send_create_signal(u'common', ['Favourite'])

        # Adding model 'Collection'
        db.create_table(u'common_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'Collection', max_length=25)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 27, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 27, 0, 0))),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('cover_album', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'cover_album', null=True, to=orm['common.Album'])),
        ))
        db.send_create_signal(u'common', ['Collection'])

        # Adding M2M table for field albums on 'Collection'
        m2m_table_name = db.shorten_name(u'common_collection_albums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collection', models.ForeignKey(orm[u'common.collection'], null=False)),
            ('album', models.ForeignKey(orm[u'common.album'], null=False))
        ))
        db.create_unique(m2m_table_name, ['collection_id', 'album_id'])

        # Adding model 'Contact'
        db.create_table(u'common_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.MokoUser'])),
        ))
        db.send_create_signal(u'common', ['Contact'])

        # Adding model 'Classified'
        db.create_table(u'common_classified', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Contact'])),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 27, 0, 0))),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 27, 0, 0))),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.MokoUser'])),
            ('meta_data', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'common', ['Classified'])


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table(u'common_album')

        # Deleting model 'Photo'
        db.delete_table(u'common_photo')

        # Removing M2M table for field video on 'Photo'
        db.delete_table(db.shorten_name(u'common_photo_video'))

        # Removing M2M table for field albums on 'Photo'
        db.delete_table(db.shorten_name(u'common_photo_albums'))

        # Deleting model 'Hospitality'
        db.delete_table(u'common_hospitality')

        # Removing M2M table for field albums on 'Hospitality'
        db.delete_table(db.shorten_name(u'common_hospitality_albums'))

        # Deleting model 'Comment'
        db.delete_table(u'common_comment')

        # Deleting model 'PhotoStory'
        db.delete_table(u'common_photostory')

        # Deleting model 'Promotion'
        db.delete_table(u'common_promotion')

        # Deleting model 'Video'
        db.delete_table(u'common_video')

        # Deleting model 'MokoUser'
        db.delete_table(u'common_mokouser')

        # Removing M2M table for field groups on 'MokoUser'
        db.delete_table(db.shorten_name(u'common_mokouser_groups'))

        # Removing M2M table for field user_permissions on 'MokoUser'
        db.delete_table(db.shorten_name(u'common_mokouser_user_permissions'))

        # Deleting model 'Favourite'
        db.delete_table(u'common_favourite')

        # Deleting model 'Collection'
        db.delete_table(u'common_collection')

        # Removing M2M table for field albums on 'Collection'
        db.delete_table(db.shorten_name(u'common_collection_albums'))

        # Deleting model 'Contact'
        db.delete_table(u'common_contact')

        # Deleting model 'Classified'
        db.delete_table(u'common_classified')


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
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'cover_photo'", 'null': 'True', 'to': u"orm['common.Photo']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 27, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 27, 0, 0)', 'null': 'True'})
        },
        u'common.classified': {
            'Meta': {'object_name': 'Classified'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Contact']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 27, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_data': ('jsonfield.fields.JSONField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MokoUser']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 27, 0, 0)'})
        },
        u'common.collection': {
            'Meta': {'object_name': 'Collection'},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Album']", 'symmetrical': 'False'}),
            'cover_album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'cover_album'", 'null': 'True', 'to': u"orm['common.Album']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 27, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u'Collection'", 'max_length': '25'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 27, 0, 0)'})
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 27, 0, 0)'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 27, 0, 0)'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_id': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'photo_owner'", 'db_column': "u'owner'", 'to': u"orm['common.MokoUser']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'times_viewed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 27, 0, 0)'}),
            'video': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Video']", 'symmetrical': 'False'})
        },
        u'common.photostory': {
            'Meta': {'ordering': "(u'-created_at',)", 'object_name': 'PhotoStory'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Album']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 27, 0, 0)'}),
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
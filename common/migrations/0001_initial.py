# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import cloudinary.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MokoUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('album_id', models.IntegerField(null=True, blank=True)),
                ('label', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('published', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Classified',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('meta_data', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='ClassifiedType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('published', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='Collection', max_length=25)),
                ('featured', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(null=True)),
                ('albums', models.ManyToManyField(to='common.Album')),
                ('cover_album', models.ForeignKey(related_name='cover_album', to='common.Album', null=True)),
            ],
            options={
                'verbose_name_plural': 'collections',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(serialize=False, primary_key=True)),
                ('image_comment', models.TextField()),
                ('comment_author', models.CharField(max_length=150)),
                ('comment_date', models.DateTimeField()),
                ('comment_approved', models.BooleanField()),
            ],
            options={
                'ordering': ('-comment_date',),
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('client_ip', models.CharField(max_length=13, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Hospitality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('featured', models.BooleanField()),
                ('hospitality_type', models.CharField(default='HOTEL', max_length=20, choices=[('HOTEL', 'Hotel'), ('RESORT', 'Resort')])),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('address', models.TextField()),
                ('telephone', models.TextField()),
                ('website', models.TextField()),
                ('contact_email', models.EmailField(default='hotelinquiry@mokocharlie.com', max_length=254)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('published', models.BooleanField(default=False)),
                ('albums', models.ManyToManyField(to='common.Album')),
            ],
            options={
                'ordering': ['-featured', '-date_added'],
                'verbose_name': 'Hospitality Provider',
                'verbose_name_plural': 'Hospitality Providers',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_id', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=250)),
                ('path', models.CharField(max_length=150, null=True, blank=True)),
                ('caption', models.TextField()),
                ('times_viewed', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Uploaded')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('published', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('cloud_image', cloudinary.models.CloudinaryField(max_length=255, null=True)),
                ('albums', models.ManyToManyField(to='common.Album')),
                ('owner', models.ForeignKey(related_name='photo_owner', db_column='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='PhotoStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('published', models.BooleanField()),
                ('album', models.ForeignKey(to='common.Album')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name_plural': 'Photo Stories',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('promo_handle', models.CharField(max_length=50, blank=True)),
                ('promo_type', models.CharField(max_length=20)),
                ('promo_name', models.CharField(max_length=150)),
                ('promo_instructions', models.TextField()),
                ('promo_album', models.IntegerField(null=True, blank=True)),
                ('static_image_path', models.CharField(max_length=250)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('featured', models.IntegerField()),
                ('published', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(max_length=150, blank=True)),
                ('external_source', models.CharField(default='YOUTUBE', max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='video',
            field=models.ManyToManyField(to='common.Video'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='photo',
            field=models.ForeignKey(to='common.Photo'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ForeignKey(to='common.Photo'),
        ),
        migrations.AddField(
            model_name='classified',
            name='contact',
            field=models.ForeignKey(to='common.Contact'),
        ),
        migrations.AddField(
            model_name='classified',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classified',
            name='type',
            field=models.ForeignKey(to='common.ClassifiedType'),
        ),
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(related_name='cover_photo', blank=True, to='common.Photo', null=True),
        ),
    ]

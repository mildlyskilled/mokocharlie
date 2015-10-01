# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_remove_hospitality_telephone'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoViews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.GenericIPAddressField()),
            ],
        ),
        migrations.RemoveField(
            model_name='photo',
            name='times_viewed',
        ),
        migrations.AddField(
            model_name='photoviews',
            name='photo',
            field=models.ForeignKey(to='common.Photo'),
        ),
        migrations.AddField(
            model_name='photoviews',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

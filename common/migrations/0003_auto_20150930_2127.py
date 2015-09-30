# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150929_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitality',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='hospitality',
            name='telephone',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='hospitality',
            name='website',
            field=models.URLField(max_length=100),
        ),
    ]

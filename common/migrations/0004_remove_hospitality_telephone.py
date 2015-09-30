# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20150930_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitality',
            name='telephone',
        ),
    ]

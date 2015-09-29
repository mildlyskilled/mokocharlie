# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitality',
            name='contact_email',
        ),
        migrations.AddField(
            model_name='hospitality',
            name='contact',
            field=models.ForeignKey(default=1, to='common.Contact'),
            preserve_default=False,
        ),
    ]

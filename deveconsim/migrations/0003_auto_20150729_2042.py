# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deveconsim', '0002_auto_20150729_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='start_cocoa',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AddField(
            model_name='turn',
            name='start_corn',
            field=models.PositiveIntegerField(default=900),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deveconsim', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turn',
            name='cocoa',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='turn',
            name='corn',
            field=models.PositiveIntegerField(default=900),
        ),
        migrations.AlterField(
            model_name='turn',
            name='land',
            field=models.PositiveIntegerField(default=1000),
        ),
    ]

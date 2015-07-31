# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deveconsim', '0006_auto_20150730_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='decapitalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='turn',
            name='voted_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='turn',
            name='debt_wb',
            field=models.PositiveIntegerField(default=750000000),
        ),
        migrations.AlterField(
            model_name='turn',
            name='debt_wbsap',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

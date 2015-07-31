# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deveconsim', '0005_auto_20150729_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='debt_new_wbsap',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='turn',
            name='debt_repay_private',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='turn',
            name='debt_repay_wb',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='turn',
            name='debt_repay_wbsap',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='turn',
            name='debt_wb',
            field=models.PositiveIntegerField(default=500000000),
        ),
        migrations.AlterField(
            model_name='turn',
            name='debt_wbsap',
            field=models.PositiveIntegerField(default=250000000),
        ),
    ]

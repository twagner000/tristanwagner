# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deveconsim', '0004_auto_20150729_2320'),
    ]

    operations = [
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

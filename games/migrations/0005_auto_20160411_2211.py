# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_bgggame_bgguser_bgguserrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bgguserrating',
            name='rating',
            field=models.FloatField(),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_auto_20160411_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='bgguserrating',
            name='numplays',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

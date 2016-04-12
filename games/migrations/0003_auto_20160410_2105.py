# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20160410_2103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bggusersearch',
            old_name='search_q',
            new_name='q',
        ),
    ]

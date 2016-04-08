# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='puzzle',
            old_name='fail_html',
            new_name='fail_template',
        ),
        migrations.RenameField(
            model_name='puzzle',
            old_name='puzzle_html',
            new_name='puzzle_template',
        ),
        migrations.RenameField(
            model_name='puzzle',
            old_name='solved_html',
            new_name='success_template',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import puzzles.models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0002_auto_20160407_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzle',
            name='puzzle_file',
            field=models.FileField(blank=True, upload_to=puzzles.models.Puzzle.puzzle_path),
        ),
    ]

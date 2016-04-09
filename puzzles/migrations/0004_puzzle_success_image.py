# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import puzzles.models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0003_auto_20160409_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='success_image',
            field=models.ImageField(upload_to=puzzles.models.Puzzle.puzzle_path, blank=True),
        ),
    ]

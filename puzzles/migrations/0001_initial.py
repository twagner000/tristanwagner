# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import puzzles.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Puzzle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('solution', models.CharField(max_length=50)),
                ('puzzle_html', models.TextField()),
                ('fail_html', models.TextField()),
                ('solved_html', models.TextField()),
                ('puzzle_file', models.FileField(upload_to=puzzles.models.Puzzle.puzzle_path)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('release_date', models.DateTimeField(null=True, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

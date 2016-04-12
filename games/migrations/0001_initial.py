# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BGGUserSearch',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('q', models.CharField(max_length=50)),
                ('users', models.TextField(blank=True)),
                ('search_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]

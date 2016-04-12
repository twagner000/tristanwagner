# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20160410_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='BGGGame',
            fields=[
                ('objectid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('yearpublished', models.IntegerField(blank=True, null=True)),
                ('minplayers', models.IntegerField(blank=True, null=True)),
                ('maxplayers', models.IntegerField(blank=True, null=True)),
                ('minplaytime', models.IntegerField(blank=True, null=True)),
                ('maxplaytime', models.IntegerField(blank=True, null=True)),
                ('playingtime', models.IntegerField(blank=True, null=True)),
                ('numowned', models.IntegerField(blank=True, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='BGGUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('user', models.CharField(max_length=250)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='BGGUserRating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('rating', models.PositiveSmallIntegerField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('game', models.ForeignKey(to='games.BGGGame')),
                ('user', models.ForeignKey(to='games.BGGUser')),
            ],
        ),
    ]

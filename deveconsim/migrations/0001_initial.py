# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('started_date', models.DateTimeField(auto_now_add=True)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('turn', models.PositiveIntegerField(default=1)),
                ('started_date', models.DateTimeField(auto_now_add=True)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('genfund', models.PositiveIntegerField(default=20000000)),
                ('debt_private', models.PositiveIntegerField(default=250000000)),
                ('debt_wb', models.PositiveIntegerField(default=500000000)),
                ('debt_wbsap', models.PositiveIntegerField(default=250000000)),
                ('tax_cocoa', models.PositiveSmallIntegerField(default=10)),
                ('tax_lower', models.PositiveSmallIntegerField(default=20)),
                ('tax_upper', models.PositiveSmallIntegerField(default=30)),
                ('svc_health', models.PositiveSmallIntegerField(default=25)),
                ('svc_education', models.PositiveSmallIntegerField(default=25)),
                ('svc_security', models.PositiveSmallIntegerField(default=35)),
                ('land', models.PositiveIntegerField(default=1000000)),
                ('corn', models.PositiveIntegerField(default=900000)),
                ('cocoa', models.PositiveIntegerField(default=100000)),
                ('landprod', models.FloatField(default=1.0)),
                ('pesticides', models.PositiveSmallIntegerField(default=0, choices=[(0, 'None'), (1, 'Cheap'), (2, 'Expensive')])),
                ('game', models.ForeignKey(to='deveconsim.Game')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='turn',
            unique_together=set([('game', 'turn')]),
        ),
    ]

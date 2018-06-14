# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-14 03:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mpatrol', '0008_auto_20180613_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='ll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mpatrol.LeaderLevel', verbose_name='Leader Level'),
        ),
    ]

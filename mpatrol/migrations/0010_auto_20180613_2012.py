# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-14 03:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpatrol', '0009_auto_20180613_2010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaderlevel',
            options={'ordering': ['level']},
        ),
        migrations.RenameField(
            model_name='leaderlevel',
            old_name='ll',
            new_name='level',
        ),
    ]

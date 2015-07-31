# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('deveconsim', '0007_auto_20150730_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turn',
            name='landprod',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='turn',
            name='svc_education',
            field=models.PositiveSmallIntegerField(default=25, validators=[django.core.validators.MaxValueValidator(100, message='Maximum is 100%%.')]),
        ),
        migrations.AlterField(
            model_name='turn',
            name='svc_health',
            field=models.PositiveSmallIntegerField(default=25, validators=[django.core.validators.MaxValueValidator(100, message='Maximum is 100%%.')]),
        ),
        migrations.AlterField(
            model_name='turn',
            name='svc_security',
            field=models.PositiveSmallIntegerField(default=35, validators=[django.core.validators.MaxValueValidator(100, message='Maximum is 100%%.')]),
        ),
        migrations.AlterField(
            model_name='turn',
            name='tax_cocoa',
            field=models.PositiveSmallIntegerField(default=10, validators=[django.core.validators.MaxValueValidator(30, message='Maximum is 30%%.')]),
        ),
        migrations.AlterField(
            model_name='turn',
            name='tax_lower',
            field=models.PositiveSmallIntegerField(default=20, validators=[django.core.validators.MaxValueValidator(70, message='Maximum is 70%%.')]),
        ),
        migrations.AlterField(
            model_name='turn',
            name='tax_upper',
            field=models.PositiveSmallIntegerField(default=30, validators=[django.core.validators.MaxValueValidator(70, message='Maximum is 70%%.')]),
        ),
    ]

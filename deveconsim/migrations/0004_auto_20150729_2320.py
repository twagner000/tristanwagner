# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('deveconsim', '0003_auto_20150729_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turn',
            name='landprod',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(0), django.core.validators.MaxValueValidator(1)], default=1.0),
        ),
        migrations.AlterField(
            model_name='turn',
            name='svc_education',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)], default=25),
        ),
        migrations.AlterField(
            model_name='turn',
            name='svc_health',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)], default=25),
        ),
        migrations.AlterField(
            model_name='turn',
            name='svc_security',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)], default=35),
        ),
        migrations.AlterField(
            model_name='turn',
            name='tax_cocoa',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(30)], default=10),
        ),
        migrations.AlterField(
            model_name='turn',
            name='tax_lower',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(70)], default=20),
        ),
        migrations.AlterField(
            model_name='turn',
            name='tax_upper',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(70)], default=30),
        ),
    ]

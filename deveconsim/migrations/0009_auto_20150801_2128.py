# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('deveconsim', '0008_auto_20150730_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='wbsap_cocoa',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='turn',
            name='debt_new_wbsap',
            field=models.PositiveIntegerField(default=0, verbose_name='New World Bank SAP Debt'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='debt_repay_private',
            field=models.PositiveIntegerField(default=0, verbose_name='Repay Private Debt'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='debt_repay_wb',
            field=models.PositiveIntegerField(default=0, verbose_name='Repay World Bank Debt'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='debt_repay_wbsap',
            field=models.PositiveIntegerField(default=0, verbose_name='Repay World Bank SAP Debt'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='svc_education',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100, message='Maximum is 100%%.')], default=25, verbose_name='Education Funding'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='svc_health',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100, message='Maximum is 100%%.')], default=25, verbose_name='Healthcare Funding'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='svc_security',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100, message='Maximum is 100%%.')], default=35, verbose_name='Security Funding'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='tax_cocoa',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(30, message='Maximum is 30%%.')], default=10, verbose_name='Cocoa Tax'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='tax_lower',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(70, message='Maximum is 70%%.')], default=20, verbose_name='Income Tax - Lower Bracket'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='tax_upper',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(70, message='Maximum is 70%%.')], default=30, verbose_name='Income Tax - Upper Bracket'),
        ),
    ]

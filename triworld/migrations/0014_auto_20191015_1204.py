# Generated by Django 2.0.6 on 2019-10-15 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triworld', '0013_auto_20191011_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='majortri',
            name='_ci',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='majortri',
            name='_ri',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]

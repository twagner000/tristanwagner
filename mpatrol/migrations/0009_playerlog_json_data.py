# Generated by Django 2.0.6 on 2018-06-29 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpatrol', '0008_auto_20180628_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerlog',
            name='json_data',
            field=models.TextField(blank=True),
        ),
    ]
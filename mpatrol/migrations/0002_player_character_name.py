# Generated by Django 2.0.6 on 2018-06-16 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpatrol', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='character_name',
            field=models.CharField(default='Thunderbolt', max_length=50),
            preserve_default=False,
        ),
    ]
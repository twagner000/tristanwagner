# Generated by Django 2.0.6 on 2018-06-29 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpatrol', '0011_auto_20180629_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['game', 'character_name']},
        ),
    ]

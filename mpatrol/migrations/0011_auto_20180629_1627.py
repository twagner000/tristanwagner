# Generated by Django 2.0.6 on 2018-06-29 23:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mpatrol', '0010_remove_player_last_action_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='player',
            unique_together={('game', 'character_name'), ('game', 'user')},
        ),
    ]

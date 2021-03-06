# Generated by Django 2.0.6 on 2018-06-30 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpatrol', '0013_player_static_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battle',
            name='attacker',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='defender',
        ),
        migrations.RemoveField(
            model_name='message',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.AddField(
            model_name='playerlog',
            name='acknowledged',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='playerlog',
            name='success',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Battle',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]

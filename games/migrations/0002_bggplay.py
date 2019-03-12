# Generated by Django 2.0.6 on 2019-03-11 02:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BGGPlay',
            fields=[
                ('bgg_play_id', models.IntegerField(primary_key=True, serialize=False)),
                ('bgg_game_id', models.IntegerField(blank=True, null=True)),
                ('game_name', models.CharField(max_length=250)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
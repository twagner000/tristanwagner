# Generated by Django 2.0.6 on 2018-06-15 04:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BGGGame',
            fields=[
                ('objectid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('yearpublished', models.IntegerField(blank=True, null=True)),
                ('minplayers', models.IntegerField(blank=True, null=True)),
                ('maxplayers', models.IntegerField(blank=True, null=True)),
                ('minplaytime', models.IntegerField(blank=True, null=True)),
                ('maxplaytime', models.IntegerField(blank=True, null=True)),
                ('playingtime', models.IntegerField(blank=True, null=True)),
                ('numowned', models.IntegerField(blank=True, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='BGGUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=250)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='BGGUserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('numplays', models.IntegerField(blank=True, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.BGGGame')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.BGGUser')),
            ],
        ),
        migrations.CreateModel(
            name='BGGUserSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q', models.CharField(max_length=50)),
                ('users', models.TextField(blank=True)),
                ('search_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]

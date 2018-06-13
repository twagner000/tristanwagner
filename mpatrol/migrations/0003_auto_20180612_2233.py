# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-13 05:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mpatrol', '0002_delete_creature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Battalion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battalion_number', models.PositiveSmallIntegerField(default=1)),
                ('creature_type', models.CharField(blank=True, choices=[('Shrew', 'Shrew'), ('Vole', 'Vole'), ('Mouse', 'Mouse'), ('Hedgehog', 'Hedgehog'), ('Squirrel', 'Squirrel'), ('Otter', 'Otter'), ('Hare', 'Hare'), ('Sparrow', 'Sparrow'), ('Owl', 'Owl'), ('Heron', 'Heron'), ('Badger', 'Badger')], max_length=50)),
                ('count', models.PositiveSmallIntegerField(default=0)),
                ('level', models.PositiveSmallIntegerField(default=1)),
                ('weapon_base', models.CharField(blank=True, choices=[('Slingshot', 'Slingshot'), ('Dagger', 'Dagger'), ('Bow', 'Bow'), ('Javelin', 'Javelin'), ('Longbow & Arrows', 'Longbow & Arrows'), ('Sword', 'Sword'), ('Armor', 'Armor')], max_length=50)),
                ('weapon_material', models.CharField(blank=True, choices=[('Wood', 'Wood'), ('Bronze', 'Bronze'), ('Iron', 'Iron'), ('Leather', 'Leather'), ('Chainmail', 'Chainmail'), ('Plate', 'Plate')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battle_date', models.DateTimeField(auto_now_add=True)),
                ('successful_attack', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('started_date', models.DateTimeField(auto_now_add=True)),
                ('ended_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('subject', models.TextField()),
                ('message', models.TextField(blank=True)),
                ('unread', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_date', models.DateTimeField(auto_now_add=True)),
                ('last_action_date', models.DateTimeField(blank=True, null=True)),
                ('ll', models.PositiveSmallIntegerField(default=1, verbose_name='Leader Level')),
                ('gold', models.PositiveIntegerField(default=0)),
                ('xp', models.PositiveIntegerField(default=0, verbose_name='Experience')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mpatrol.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='mpatrol.Player'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='mpatrol.Player'),
        ),
        migrations.AddField(
            model_name='battle',
            name='attacker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attacker', to='mpatrol.Player'),
        ),
        migrations.AddField(
            model_name='battle',
            name='defender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defender', to='mpatrol.Player'),
        ),
        migrations.AddField(
            model_name='battalion',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mpatrol.Player'),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('game', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='battalion',
            unique_together=set([('player', 'battalion_number')]),
        ),
    ]

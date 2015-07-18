# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnsweredChecklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('for_date', models.DateField(default=django.utils.timezone.now)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('ans_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnsweredQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(blank=True)),
                ('ans_checklist', models.ForeignKey(to='checklist.AnsweredChecklist')),
            ],
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('public', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('question', models.CharField(max_length=200)),
                ('sequence', models.PositiveIntegerField(default=10)),
                ('weight', models.PositiveIntegerField(default=10)),
                ('help', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['question_group', 'sequence'],
            },
        ),
        migrations.CreateModel(
            name='QuestionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('sequence', models.PositiveIntegerField(default=10)),
                ('help', models.TextField(blank=True)),
                ('checklist', models.ForeignKey(to='checklist.Checklist')),
            ],
            options={
                'ordering': ['checklist', 'sequence'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='question_group',
            field=models.ForeignKey(to='checklist.QuestionGroup'),
        ),
        migrations.AddField(
            model_name='answeredquestion',
            name='question',
            field=models.ForeignKey(to='checklist.Question'),
        ),
        migrations.AddField(
            model_name='answeredchecklist',
            name='checklist',
            field=models.ForeignKey(to='checklist.Checklist'),
        ),
    ]

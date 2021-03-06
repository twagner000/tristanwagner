# Generated by Django 2.0.6 on 2018-06-15 04:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnsweredChecklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_date', models.DateField(default=django.utils.timezone.now)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('ans_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnsweredQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(blank=True)),
                ('ans_checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checklist.AnsweredChecklist')),
            ],
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('public', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('sequence', models.PositiveIntegerField(default=10)),
                ('help', models.TextField(blank=True)),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checklist.Checklist')),
            ],
            options={
                'ordering': ['checklist', 'sequence'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='question_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checklist.QuestionGroup'),
        ),
        migrations.AddField(
            model_name='answeredquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checklist.Question'),
        ),
        migrations.AddField(
            model_name='answeredchecklist',
            name='checklist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checklist.Checklist'),
        ),
    ]

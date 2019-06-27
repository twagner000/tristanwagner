# Generated by Django 2.0.6 on 2019-06-27 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetracker', '0003_remove_project_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='hours',
            field=models.FloatField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='project',
            name='top_level_project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_set_all_levels', to='timetracker.Project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_set', to='timetracker.Project'),
        ),
    ]

# Generated by Django 2.0.6 on 2019-10-05 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triworld', '0003_auto_20191004_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='face',
            name='neighbor_ids',
            field=models.TextField(blank=True, editable=False),
        ),
    ]

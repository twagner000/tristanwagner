# Generated by Django 2.0.6 on 2018-06-21 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpatrol', '0002_player_character_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='technology',
            options={'ordering': ['level', 'cost_xp', 'name']},
        ),
        migrations.RenameField(
            model_name='technology',
            old_name='cost',
            new_name='cost_xp',
        ),
    ]
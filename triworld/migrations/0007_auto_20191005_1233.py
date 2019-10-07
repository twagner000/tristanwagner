# Generated by Django 2.0.6 on 2019-10-05 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('triworld', '0006_auto_20191005_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaceExt',
            fields=[
                ('face', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='triworld.Face')),
                ('points_down', models.BooleanField(default=None)),
                ('neighbor_ids', models.TextField(default='null')),
                ('map', models.TextField(default='null')),
            ],
            options={
                'ordering': ['face'],
            },
        ),
        migrations.RemoveField(
            model_name='facejson',
            name='face',
        ),
        migrations.AlterField(
            model_name='face',
            name='face_index',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='face',
            name='face_ring',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='face',
            name='world',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triworld.World'),
        ),
        migrations.AlterField(
            model_name='majortri',
            name='face',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triworld.Face'),
        ),
        migrations.AlterField(
            model_name='majortri',
            name='major_col',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='majortri',
            name='major_row',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='majortri',
            name='sea',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='minortri',
            name='minor_col',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='minortri',
            name='minor_row',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='world',
            name='major_dim',
            field=models.PositiveSmallIntegerField(default=6, help_text='Number of major triangles per face edge.'),
        ),
        migrations.AlterField(
            model_name='world',
            name='minor_dim',
            field=models.PositiveSmallIntegerField(default=6, help_text='Number of minor triangles per major triangle edge.'),
        ),
        migrations.DeleteModel(
            name='FaceJSON',
        ),
        migrations.AddIndex(
            model_name='faceext',
            index=models.Index(fields=['face'], name='triworld_fa_face_id_92bf56_idx'),
        ),
    ]
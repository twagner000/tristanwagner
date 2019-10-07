# Generated by Django 2.0.6 on 2019-10-05 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('triworld', '0002_auto_20191004_2332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Face',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('face_ring', models.PositiveSmallIntegerField(editable=False)),
                ('face_index', models.PositiveSmallIntegerField(editable=False)),
            ],
            options={
                'ordering': ['world', 'face_ring', 'face_index'],
            },
        ),
        migrations.CreateModel(
            name='MajorTri',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_row', models.PositiveSmallIntegerField(editable=False)),
                ('major_col', models.PositiveSmallIntegerField(editable=False)),
                ('sea', models.BooleanField(default=True, editable=False)),
                ('face', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='triworld.Face')),
            ],
            options={
                'ordering': ['face', 'major_row', 'major_col'],
            },
        ),
        migrations.CreateModel(
            name='MinorTri',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minor_row', models.PositiveSmallIntegerField(editable=False)),
                ('minor_col', models.PositiveSmallIntegerField(editable=False)),
                ('major_tri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triworld.MajorTri')),
            ],
            options={
                'ordering': ['major_tri', 'minor_row', 'minor_col'],
            },
        ),
        migrations.CreateModel(
            name='World',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_dim', models.PositiveSmallIntegerField(default=6, editable=False, help_text='Number of major triangles per face edge.')),
                ('minor_dim', models.PositiveSmallIntegerField(default=6, editable=False, help_text='Number of minor triangles per major triangle edge.')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.AddField(
            model_name='face',
            name='world',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='triworld.World'),
        ),
        migrations.AddIndex(
            model_name='minortri',
            index=models.Index(fields=['major_tri', 'minor_row', 'minor_col'], name='triworld_mi_major_t_e23a73_idx'),
        ),
        migrations.AddIndex(
            model_name='minortri',
            index=models.Index(fields=['major_tri'], name='triworld_mi_major_t_4979ad_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='minortri',
            unique_together={('major_tri', 'minor_row', 'minor_col')},
        ),
        migrations.AddIndex(
            model_name='majortri',
            index=models.Index(fields=['face', 'major_row', 'major_col'], name='triworld_ma_face_id_ef8fa3_idx'),
        ),
        migrations.AddIndex(
            model_name='majortri',
            index=models.Index(fields=['face'], name='triworld_ma_face_id_6984c7_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='majortri',
            unique_together={('face', 'major_row', 'major_col')},
        ),
        migrations.AddIndex(
            model_name='face',
            index=models.Index(fields=['world', 'face_ring', 'face_index'], name='triworld_fa_world_i_ee88fc_idx'),
        ),
        migrations.AddIndex(
            model_name='face',
            index=models.Index(fields=['world'], name='triworld_fa_world_i_b2f750_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='face',
            unique_together={('world', 'face_ring', 'face_index')},
        ),
    ]
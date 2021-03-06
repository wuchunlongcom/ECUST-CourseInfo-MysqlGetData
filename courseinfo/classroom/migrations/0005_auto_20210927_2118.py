# Generated by Django 2.2.6 on 2021-09-27 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0004_auto_20210927_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='building',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='classroom.Building'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='classroomType',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='classroom.ClassroomType'),
        ),
    ]

# Generated by Django 2.2.7 on 2020-09-14 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0009_auto_20200914_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roleId',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, to='online.Role'),
        ),
    ]

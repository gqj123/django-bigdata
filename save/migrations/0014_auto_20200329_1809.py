# Generated by Django 2.2.7 on 2020-03-29 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('save', '0013_auto_20191206_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='file_record',
            name='contact_num',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='file_record',
            name='data_cont',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='file_record',
            name='data_desc',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='file_record',
            name='data_type',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='file_record',
            name='data_vol',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='file_record',
            name='direction',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='file_record',
            name='space_res',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='file_record',
            name='time_res',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='file_record',
            name='update_freq',
            field=models.CharField(default='', max_length=30),
        ),
    ]

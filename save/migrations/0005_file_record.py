# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-14 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('save', '0004_remove_useraction_int'),
    ]

    operations = [
        migrations.CreateModel(
            name='file_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('content_type', models.IntegerField()),
                ('file_type', models.IntegerField()),
                ('introduce', models.CharField(max_length=20000)),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-19 11:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0007_auto_20180607_1715'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': '\u5df2\u6ce8\u518c\u7528\u6237'},
        ),
        migrations.AlterModelOptions(
            name='userlogin',
            options={'verbose_name_plural': '\u7528\u6237\u767b\u5f55\u8bb0\u5f55'},
        ),
    ]
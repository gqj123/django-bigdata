# Generated by Django 2.2.7 on 2020-09-14 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online', '0008_auto_20180719_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('wenjianxiyuan', models.CharField(default='1', max_length=10)),
                ('hbaseshujuku', models.CharField(default='1', max_length=10)),
                ('shouye', models.CharField(default='1', max_length=10)),
                ('ziyuanguanli', models.CharField(default='1', max_length=10)),
                ('ziyuanchaxun', models.CharField(default='1', max_length=10)),
                ('suanfaziyuan', models.CharField(default='1', max_length=10)),
                ('moxingziyuan', models.CharField(default='1', max_length=10)),
                ('suanfachaxun', models.CharField(default='1', max_length=10)),
                ('yanshi', models.CharField(default='1', max_length=10)),
                ('tijao', models.CharField(default='1', max_length=10)),
                ('shujuku', models.CharField(default='1', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rolename', models.CharField(max_length=20)),
                ('permissionid', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='roleId',
            field=models.CharField(default='2', max_length=20),
        ),
    ]
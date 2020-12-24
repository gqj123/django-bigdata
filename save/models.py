# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
# Create your models here.
class Useraction(models.Model):
    username=models.CharField(max_length=50)
    actiontime=models.DateTimeField(auto_now=True)
    action=models.CharField(max_length=200)
    #int=models.IntegerField(default=0)
    class Meta:
        verbose_name_plural='用户操作'
    def __str__(self):
        return self.username
class actionadmin(admin.ModelAdmin):
    list_display = ('username','actiontime','action')


class file_record(models.Model):
    file_name=models.CharField(max_length=200)

    data_name=models.CharField(max_length=30)
    data_source=models.CharField(max_length=30)
    class_name=models.CharField(max_length=20000)
    important=models.CharField(max_length=2000,default="")
    time=models.CharField(max_length=2000,default="")
    place=models.CharField(max_length=2000,default="")
    file_path=models.CharField(max_length=2000,default="")

    # 应用方向
    direction=models.CharField(max_length=30, default="")
    # 数据种类
    data_type=models.CharField(max_length=30, default="")
    # 时间分辨率
    time_res=models.CharField(max_length=30, default="")
    # 空间分辨率
    space_res=models.CharField(max_length=30, default="")
    # 数据集联系人
    data_cont=models.CharField(max_length=30, default="")
    # 联系电话
    contact_num=models.CharField(max_length=30, default="")
    # 更新频率
    update_freq=models.CharField(max_length=30, default="")
    # 数据量
    data_vol=models.CharField(max_length=30, default="")
    # 数据格式说明
    data_desc=models.CharField(max_length=30, default="")

    class Meta:
        verbose_name_plural='上传文件记录'
    def __str__(self):
        return self.username

class function_model(models.Model):
    function_name=models.CharField(max_length=200,blank=True,null=True)
    file_name=models.CharField(max_length=200,default="",blank=True,null=True)
    function_type=models.CharField(max_length=200,blank=True,null=True)
    upload_user=models.CharField(max_length=200,blank=True,null=True)
    input_files_path=models.CharField(max_length=200,blank=True,null=True)
    output_files_path=models.CharField(max_length=200,blank=True,null=True)
    parameter=models.CharField(max_length=200,blank=True,null=True)
    introduce=models.CharField(max_length=50000,blank=True,null=True)
    function_class = models.IntegerField(blank=True,null=True)
    class Meta:
        verbose_name_plural='大数据方法'
    def __str__(self):
        return self.function_name

class Picture(models.Model):

    img_url =models.ImageField("图片",upload_to="mypicture")
    def __str__(self):
        return self.title


class file_record_admin(admin.ModelAdmin):
    list_display = ('file_name','data_name','data_source','class_name',"important","time","place","file_path")

class function_admin(admin.ModelAdmin):
    list_display = ('function_name','function_type','upload_user','input_files_path','output_files_path','parameter','introduce','file_name','function_class')

admin.site.register(Useraction,actionadmin)
admin.site.register(file_record,file_record_admin)
admin.site.register(function_model,function_admin)

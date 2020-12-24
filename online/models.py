# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.
class User(models.Model):
    class Meta:
        verbose_name_plural='已注册用户'
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email=models.CharField(max_length=100,default='')
    employer=models.CharField(max_length=100,default='')
    tel=models.CharField(max_length=100,default='')
    level=models.IntegerField(default=1)
    created_time=models.DateTimeField(auto_now_add=True)
    # 角色id；1超级管理员 2 普通用户 3 游客
    role = models.ForeignKey('Role', on_delete=models.CASCADE, default='2')

    def __unicode__(self):
        return self.username

#角色表，和用户表 用roidId连在一起
class Role(models.Model):
    rolename = models.CharField(max_length=20)
    permission = models.ForeignKey('Permission', on_delete=models.CASCADE, default='1')


#权限表， 一个角色对应一条记录
class Permission(models.Model):
    name = models.CharField(max_length=20)
    #这里有点多，我用拼音来写的,1 代表可以查看这个菜单
    wenjianziyuan = models.CharField(max_length=10,default='1')  # 文件资源
    hbaseshujuku  = models.CharField(max_length=10,default='1')  # hbase数据库
    moxingsuanfa  = models.CharField(max_length=10,default='1')  # 模型算法
    shouye        = models.CharField(max_length=10,default='1')  # 首页
    ziyuanguanli  = models.CharField(max_length=10,default='1')  # 资源管理
    ziyuanchaxun  = models.CharField(max_length=10,default='1')  # 资源查询
    jiqunchakan   = models.CharField(max_length=10,default='1')  # 集群查看
    suanfaziyuan  = models.CharField(max_length=10,default='1')  # 算法资源
    moxingziyuan  = models.CharField(max_length=10,default='1')  # 模型资源
    suanfachaxun  = models.CharField(max_length=10,default='1')  # 算法查询
    yanshi        = models.CharField(max_length=10,default='1')  # 演示
    tijao         = models.CharField(max_length=10,default='1')  # 提交
    shujuku       = models.CharField(max_length=10,default='1')  # 数据库

class Userlogin(models.Model):

   username=models.CharField(max_length=50)
   logintime=models.DateTimeField(auto_now=True)
   class Meta:
       verbose_name_plural='用户登录记录'

class Useradmin(admin.ModelAdmin):
    list_display = ('username','password','created_time',"level","email","employer","tel")


class loginadmin(admin.ModelAdmin):
  list_display = ('username','logintime')


admin.site.register(User,Useradmin)
admin.site.register(Userlogin,loginadmin)
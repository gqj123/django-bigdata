# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models
from student.models import student
# Register your models here.
class student_admin(admin.ModelAdmin):
    list_display = ['id','data_soure','class1','class2','class3','time_year','time_month','filename','path']
admin.site.register(models.student,student_admin)
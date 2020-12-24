# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# from hdfs import *


class student(models.Model):
    data_soure = models.CharField(max_length=50)
    class1 = models.CharField(max_length=50)
    class2 = models.CharField(max_length=50)
    class3 = models.CharField(max_length=50)
    class4 = models.CharField(max_length=50)
    time_year = models.CharField(max_length=50)
    time_month = models.CharField(max_length=50)
    filename = models.CharField(max_length=80)
    path = models.CharField(max_length=100)
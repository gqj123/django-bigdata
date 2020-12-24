# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from hdfs import *
from student.models import student
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#从sea中导入的
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext


# Create your views here.
def index(request):#这一个方法是新添�?
    pass

#链接hdfs网址
def connect():
    # client = Client("http://202.199.10.22:50070",root="/",timeout=300000,session=False)
    client = Client("http://221.239.0.181:50070",root="/",timeout=300000,session=False)
    return client

#遍历所有的文件夹并且插入到数据库中
def get_all_file(filepath):
    client = connect()
    if filepath=="/":
        pass
    else:
        filepath=filepath+"/"
    j=0
    #遍历所有的文件�?
    for root,dir,files in client.walk(filepath):
        for file in files:
            full_path=os.path.join(root,file)  #所有的路径
            str = root                         #根路�?
            a = file                           #文件�?
            #测试代码
            # b = '/'
            # c = str+b
            # d = c+a
            # print(d)
            # print(file)
            # print(full_path)
            #把路径进行分割存入到数据库中
            c = str.split("/")
            a=[]
            i=0
            while i<8:
                a.append(0)
                i+=1
            length = len(c)
            i=0
            while i<length:
                a[i]=c[i]
                if a[i].isdigit():
                    if len(a[i])==4:
                        a[6]=a[i]
                    else:
                        a[7]=a[i]
                i+=1
            data_soure= a[1]
            class1 = a[2]
            class2 =a[3]
            class3 =a[4]
            class4 = a[5]
            time_year = a[6]
            time_month = a[7]
            filename=file
            path=root
            #插入数据�?
            student.objects.create(data_soure=data_soure,class1=class1,class2=class2,class3=class3,class4=class4,time_year=time_year,time_month=time_month,filename=filename,path=path)

#插入激活函�?    当需要插入文件时执行一次就可以�?
# get_all_file("/hydrom_data_TS/")#遍历那个文件�?
# get_all_file("/grid_test/")#遍历那个文件�?

#删除所有数据库中的数据
def delete(args):
    if args==1:
        student.objects.all().delete()
# 删除激活函�?
# delete(1)


from django.http import JsonResponse
def updatesystem(request):
    username = request.COOKIES.get('username','level')
    print(username)
    if(username=='level'):
        return render(request,'login.html')
    if request.method=="POST":
        pass
    else:
        try:
            dnsnamelist=student.objects.all().values("data_soure").distinct()
        except Exception:
            return render(request,"updatesystem.html",{"login_err":"loaddnsnamefail","chooseIndex": "6"})
        return render(request,"updatesystem.html",{"dnsnamelist":dnsnamelist,"username":username,"chooseIndex": "6"})


def getipaddr(request):
    if request.method == 'GET':
        seldnsname=request.GET.get('seldnsname')
        if seldnsname:
            data =list(student.objects.filter(data_soure=seldnsname).values("class1").distinct())
            return JsonResponse(data, safe=False)

def getipaddr1(request):
    if request.method == 'GET':
        selhostipaddrs=request.GET.get('selhostipaddrs')
        if selhostipaddrs:
            data1 =list(student.objects.filter(class1=selhostipaddrs).values("class2").distinct())
            return JsonResponse(data1, safe=False)


# 修改selhostipaddrs1
def getipaddr2(request):
    if request.method == 'GET':
        selhostipaddrs1=request.GET.get('selhostipaddrs1')
        if selhostipaddrs1:
            data2 =list(student.objects.filter(class2=selhostipaddrs1).values("time_year").distinct())
            return JsonResponse(data2, safe=False)

def getipaddr3(request):
    if request.method == 'GET':
        selhostipaddrs2=request.GET.get('selhostipaddrs2')
        if selhostipaddrs2:
            data3 =list(student.objects.filter(time_year=selhostipaddrs2).values("time_month").distinct())
            print(data3)
            print("---")
            return JsonResponse(data3, safe=False)
#
def getipaddr4(request):
    if request.method == 'GET':
        selhostipaddrs3=request.GET.get('selhostipaddrs3')
        selhostipaddrs2=request.GET.get('selhostipaddrs2')
        selhostipaddrs1=request.GET.get('selhostipaddrs1')
        selhostipaddrs=request.GET.get('selhostipaddrs')
        if selhostipaddrs3 and selhostipaddrs2 and selhostipaddrs1 and selhostipaddrs:
            data4 =list(student.objects.filter(class1=selhostipaddrs,class2=selhostipaddrs1,time_year=selhostipaddrs2,time_month=selhostipaddrs3).values("filename"))
            return JsonResponse(data4, safe=False)

def getipaddr5(request):
    if request.method == 'GET':
        selhostipaddrs4=request.GET.get('selhostipaddrs4')
        if selhostipaddrs4:
            data5 =list(student.objects.filter(filename=selhostipaddrs4).values("path").distinct())
            # path1=student.objects.filter(filename=selhostipaddrs4).values("path").distinct()
            # print(path1)
            return JsonResponse(data5, safe=False)

def addpath(request):
    if request.method=="POST":
        u = request.POST.get("path1",None)
        same_name_user=student.objects.filter(data_soure=u)
        if same_name_user:
            message = "已存在?"
            print("已存在?")
            return HttpResponse("路径已存在，请重新输入?")
            # return render(request,'updatesystem.html',{"message":"路径已存在，请重新输�?})
        else:
            try:
                get_all_file(u)
                print("存取ok")
            except:
                return HttpResponse("输入路径不正确，请重新输入?")
                # return render(request,'updatesystem.html',{"message":"输入路径不正确，请重新输�?})
        return HttpResponse("存取成功")
        # return render(request,"updatesystem.html",{"message":"存取成功"})

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *
import re
import sys
import time
import os


# def hbasecheck(request):
#     username = request.COOKIES.get('username', 'level')
#     print(username)
#     if (username == 'level'):
#         return render(req,'login.html')
#     return render(request, "hbase.html", {"chooseIndex": "7"})



def hbaseTable(request, tableName):
    # 应该是可以的
    # stack = request.session.get('page', default=[])
    # stack.append(tableName)
    # request.session['page'] = stack

    # print('-' * 20)
    # print(stack)

    print(tableName)

    transport = TSocket.TSocket('221.239.0.181', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Hbase.Client(protocol)
    transport.open()

    startKey, lastKey = '', ''
    list_dict = []
    start_t, stop_t, lat_start, lat_stop, lon_start, lon_stop = '0', '2100', '0', '180.00', '0', '360.00'
    pageflag = 0
    pagenum = 0
    if request.method == "POST":
        if 'start_t' in request.POST:
            start_t = request.POST['start_t']

        if 'stop_t' in request.POST:
            stop_t = request.POST['stop_t']

        if 'lat_start' in request.POST:
            lat_start = request.POST['lat_start']

        if 'lat_stop' in request.POST:
            lat_stop = request.POST['lat_stop']

        if 'lon_start' in request.POST:
            lon_start = request.POST['lon_start']

        if 'lon_stop' in request.POST:
            lon_stop = request.POST['lon_stop']

        startKey = start_t
        stopKey= stop_t
        # startKey = str(start_t).ljust(10, '0') + '_' + str("%3.2f" % float(lat_start)).rjust(6, '0') + '_' + str("%3.2f" % float(lon_start)).rjust(6, '0')
        # stopKey = str(stop_t).ljust(10, '0') + '_' + str("%3.2f" % float(lat_stop)).rjust(6, '0') + '_' + str("%3.2f" % float(lon_stop)).rjust(6, '0')


        if 'pagedown' in request.POST:  # 下页的操作
            if 'pagenum' in request.POST:
                pagenum = int(request.POST['pagenum'])
            # startKey = request.POST['pagedown']
            # tem = request.POST['startKey']

            # 下一页需要在session中取出startkey
            stack = request.session.get('page', default=[])
            startKey = stack[-1]
            pagenum = pagenum + 30

        elif 'pageup' in request.POST: # 上一页的操作
            if 'pagenum' in request.POST:
                pagenum = int(request.POST['pagenum'])

            stack = request.session.get('page', default=[])
            if(len(stack)>2):
                stack.pop()
                stack.pop()
            startKey = stack[-1]
            pagenum = pagenum - 30

        else: # 直接点击查询的操作
            del request.session['page']

            stack = request.session.get('page', default=[])
            stack.append(startKey)
            request.session['page'] = stack


        list_dict = tableData(tableName, startKey, stopKey, lat_start, lon_start, lat_stop, lon_stop, client)

    else:

        # 普通查询

        list_dict = tableData(tableName,start_t,stop_t,lat_start,lon_start,lat_stop,lon_stop, client)
        # 页面转过来的第一次需要存储startkey
        del request.session['page']

        stack = request.session.get('page', default=[])

        startKey = list_dict[0]["rowKey"]
        # lastKey = list_dict[-1]["rowKey"]
        stack.append(startKey)
        # stack.append(lastKey)

        request.session['page'] = stack

    if list_dict:
        lastKey = list_dict[-1]["rowKey"]
        list_dict = list_dict[0:-1]  # 去掉最后一行
        # 每次将第101条的数据的id 存进session 作为下一页的startKey
        stack = request.session.get('page', default=[])
        stack.append(lastKey)
        request.session['page'] = stack
    transport.close()
    return render(request, 'hbase.html', {"tableName": tableName, 'objects': list_dict, "chooseIndex": "7",
                                          "startKey": startKey, "lastKey": lastKey,
                                          "start_t": start_t, "stop_t": stop_t,
                                          "lat_start": lat_start, "lat_stop": lat_stop,
                                          "lon_start": lon_start, "lon_stop": lon_stop,
                                          "pageflag": pageflag, "pagenum": pagenum})

def tableData(tableName,startKey, stopKey, lat_start,lon_start,lat_stop,lon_stop,client):

    list_list = []

    lat_start = str("%3.2f" % float(lat_start)).rjust(6, '0')
    lat_stop = str("%3.2f" % float(lat_stop)).rjust(6, '0')

    lon_start = str("%3.2f" % float(lon_start)).rjust(6, '0')
    lon_stop = str("%3.2f" % float(lon_stop)).rjust(6, '0')


    scanner = client.scannerOpenWithStop(tableName, startKey, stopKey, [])


    count = 0
    while True:
        if count >= 31: break
        result = client.scannerGet(scanner)
        if not result:break
        for dir in result:
            dict = {}
            dict["rowKey"] = dir.row
            dict["time"] = dir.columns.get('info:time').value
            dict["lat"] = dir.columns.get('info:lat').value
            dict["lon"] = dir.columns.get('info:lon').value

            if (tableName == "WL"):
                dict["w_level"] = dir.columns.get('info:w_level').value
            if (tableName == "AT"):
                dict["a_temperature"] = dir.columns.get('info:a_temperature').value
            if (tableName == "SLP"):
                dict["pressure"] = dir.columns.get('info:pressure').value
            if (tableName == "SST"):
                dict["w_temperature"] = dir.columns.get('info:w_temperature').value
            if (tableName == "WIND"):
                dict["direction"] = dir.columns.get('info:direction').value
                dict["speed"] = dir.columns.get('info:speed').value
            if (tableName == "PSAL"):
                dict["deep"] = dir.columns.get('info:deep').value
                dict["deep_qc"] = dir.columns.get('info:deep_qc').value
                dict["salinity"] = dir.columns.get('info:salinity').value
                dict["salinity_qc"] = dir.columns.get('info:salinity_qc').value
            if (tableName == "TEMP"):
                dict["deep"] = dir.columns.get('info:deep').value
                dict["deep_qc"] = dir.columns.get('info:deep_qc').value
                dict["temperature"] = dir.columns.get('info:temperature').value
                dict["temperature_qc"] = dir.columns.get('info:temperature_qc').value
            if (tableName == "STATION-TEMP"):
                dict["deep"] = dir.columns.get('info:deep').value
                dict["temperature"] = dir.columns.get('info:temperature').value
            if (tableName == "STATION-PSAL"):
                dict["deep"] = dir.columns.get('info:deep').value
                dict["salinity"] = dir.columns.get('info:salinity').value
            if (tableName == "STATION-CUR"):
                dict["depth"] = dir.columns.get('info:depth').value
                dict["direction"] = dir.columns.get('info:direction').value
                dict["speed"] = dir.columns.get('info:speed').value

            if dict["lat"] >= lat_start and dict["lon"] >= lon_start and dict["lat"] <= lat_stop and dict["lon"] <= lon_stop:
                list_list.append(dict)
                print(dict)
                count = count + 1
    return list_list

# def tableData(tableName, startKey, stopKey, client):
#     print('-'*20 + startKey)
#
#     if stopKey == '0000000000_000.00_000.00': stopKey = ''
#     print('-' * 20 + stopKey)
#     list_dict = []
#
#     scanner = client.scannerOpenWithStop(tableName, startKey, stopKey, [])
#     result = client.scannerGetList(scanner, 101)
#     for dir in result:
#         dict = {}
#         dict["rowKey"] = dir.row
#         dict["time"] = dir.columns.get('info:time').value
#         dict["lat"] = dir.columns.get('info:lat').value
#         dict["lon"] = dir.columns.get('info:lon').value
#
#         if (tableName == "WL"):
#             dict["w_level"] = dir.columns.get('info:w_level').value
#         if (tableName == "AT"):
#             dict["a_temperature"] = dir.columns.get('info:a_temperature').value
#         if (tableName == "SLP"):
#             dict["pressure"] = dir.columns.get('info:pressure').value
#         if (tableName == "SST"):
#             dict["w_temperature"] = dir.columns.get('info:w_temperature').value
#         if (tableName == "WIND"):
#             dict["direction"] = dir.columns.get('info:direction').value
#             dict["speed"] = dir.columns.get('info:speed').value
#         if (tableName == "PSAL"):
#             dict["direction"] = dir.columns.get('info:deep').value
#             dict["deep_qc"] = dir.columns.get('info:deep_qc').value
#             dict["salinity"] = dir.columns.get('info:salinity').value
#             dict["salinity_qc"] = dir.columns.get('info:salinity_qc').value
#         if (tableName == "TEMP"):
#             dict["deep"] = dir.columns.get('info:deep').value
#             dict["deep_qc"] = dir.columns.get('info:deep_qc').value
#             dict["temperature"] = dir.columns.get('info:temperature').value
#             dict["temperature_qc"] = dir.columns.get('info:temperature_qc').value
#         if (tableName == "STATION-TEMP"):
#             dict["deep"] = dir.columns.get('info:deep').value
#             dict["temperature"] = dir.columns.get('info:temperature').value
#         if (tableName == "STATION-PSAL"):
#             dict["deep"] = dir.columns.get('info:deep').value
#             dict["salinity"] = dir.columns.get('info:salinity').value
#         if (tableName == "STATION-CUR"):
#             dict["depth"] = dir.columns.get('info:depth').value
#             dict["direction"] = dir.columns.get('info:direction').value
#             dict["speed"] = dir.columns.get('info:speed').value
#         list_dict.append(dict)
#     return list_dict



def sparkcheck(request):
    # username=username
    username = request.COOKIES.get('username','level')
    print(username)
    if(username=='level'):
        return render(request,'login.html')
    return render(request,"spark_check.html",{"username":username})


def filedata(request, file_code):
    username = request.COOKIES.get('username', 'level')
    print(username)
    if (username == 'level'):
        return render(request,'login.html')
    if file_code == '0':
        return render(request,"firstpage0.html", {"file_code": "file_0", 'username': username, 'chooseIndex': '0'})
    if file_code == '1':
        return render(request,"firstpage1.html", {"file_code": "file_1", 'username': username, 'chooseIndex': '0'})
    if file_code == '2':
        return render(request,"firstpage2.html", {"file_code": "file_2", 'username': username, 'chooseIndex': '0'})
    if file_code == '3':
        return render(request,"firstpage3.html", {"file_code": "file_3", 'username': username, 'chooseIndex': '0'})
    if file_code == '4':
        return render(request,"firstpage4.html", {"file_code": "file_4", 'username': username, 'chooseIndex': '0'})


def testhdfs (request):
    path = request.GET.get('path')
    from save.actionhdfs import get_hdfs_file
    # path = path[5:]

    try:
        mess_list = get_hdfs_file(path)
    except:
        mess_list = []
    return render(request, "hdfsfile.html", {
        "mess_list": mess_list,
        "path_value": path
    })

def downhdfs (request):
    file_path = request.GET.get('path')
    print('你走到这里了吗,是不是又迷路啦啊' + file_path)
    from save.actionhdfs import down_file
    # file_path = "http:\/\/221.239.0.181:50070/explorer.html#/" + file_path[:-1]
    # file_path = file_path[1:]
    # down_file(file_path, 'C:\\Users\\baron\\Downloads\\')

    from pyhdfs import HdfsClient

    client = HdfsClient(hosts='221.239.0.181:50070')

    client.copy_to_local(file_path, 'C:')

    return render(request, "hdfsfile.html", {
        "mess_list": [],
        "path_value": file_path
    })

    action1 = ""
    # action1="download  "+file_path+" "+" to "+name
    # lenth = len(file_path)
    # count = 0
    # string1 = ''
    # string = file_path[::-1]
    # for i in range(0, lenth):
    #     if string[i] == '/':
    #         string1 = string[0:i]
    #         break
    #     i += 1
    # string1 = string1[::-1]
    # open_path = 'C:\\Users\\baron\\Downloads\\' + string1
    # file = open(open_path, 'rb')
    # # mm='/usr/hubingtest/胡兵model12321.py'.encode('utf-8').decode('ISO-8859-1')
    # # file=open(mm,'rb')
    # response = FileResponse(file)
    # response['Content-Type'] = 'application/octet-stream'
    # response['Content-Disposition'] = 'attachment;filename="{}"'.format(string1).encode('utf-8').decode('ISO-8859-1')
    #
    # return response

from django.http import FileResponse

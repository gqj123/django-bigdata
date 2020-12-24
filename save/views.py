# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render

# Create your views here.
#-*-coding:utf-8-*-
from django.shortcuts import render_to_response
from django.http   import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from save.models import *
from online import  models
from save import models
from django.http import FileResponse
import logging
import logging.config
import  sys
from save.actionhdfs import get_child_list,down_file,upload_file

# def getlevel(username):
#     level1=models.User.objects.values('level').get(username=username)
#     level2=level1.values()
#     level=level2[0]
#   #  logging.config.fileConfig('logging.conf')
#     logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     logger = logging.getLogger('level is')
#
#     logger.info(level)
#     logger.info(level1)
#     logger.info(level2)
#
#     return level
# Create your views here.
@csrf_exempt
def hdfsfile(request,username):
    # level=getlevel(username)
    # logger.info(level)
    print(username)
    if(username=='level'):
        return  render(request,"login.html")

    from save.actionhdfs import get_all_file
    #如果是用户提交查询
    if request.method=="POST":
        path = request.POST.get("filepath")

        #level=int(getlevel(username))
        # level=getlevel(username)
        #
        # if level==1:
        #     path="/1"
        # elif level==2:
        #     path="/2"
        # else:path="/3"
        if path == "/":
            root_more=0
        else:
            root_more=1
        error=0
        try:
            mess_list = get_all_file(path)
        except:
            error="路径不存在或者为文件!"
            mess_list=[]
        return render(request,"index.html", {
            "mess_list": mess_list,
            "path_value":path,
            "error":error,
            "root_more":root_more,
             "name":username,
            'chooseIndex':'1',
            # "level":level,
        })
    #如果是url直接定位到该界面，默认返回/
    else:
        #level=int(getlevel(username))
        # level=getlevel(username)
        #logging(level.values())
        # if level==1:
        #     path="/1"
        # elif level==2:
        #     path="/2"
        # else:
        #     path="/3"
        path="/"
       # mess_list = get_all_file(path)
       #只显示部分目录   5.24修改的
        test2=get_all_file(path)
        mess_list = []
        for mess in test2:
            #对应部分目录的ip14 data2019 21 kj 22 kj_out  23 kj_test
            if mess==test2[14] or mess==test2[21] or mess==test2[22] or mess==test2[23]:
               # print("mess is:",mess)
                mess_list.append(mess)

        return render(request,"index.html",{
            "mess_list":mess_list,
            "path_value":path,
            "root_more":0,
            "name":username,
            "chooseIndex":'1',
        })

#直接点击目录名进行下一级的查看
@csrf_exempt
def file(request,username,path):
    if(username=='level'):
        return  render(request,"login.html")
    from save.actionhdfs import get_all_file
    path = path[5:]
    if path=="":
        root_more=0
    else:
        root_more=1
    try:
        error=0
        mess_list = get_all_file(path)
    except:
        mess_list=[]
        error="路径不存在或者为文件!"
    return render(request,"index.html", {
        "mess_list": mess_list,
        "path_value": path,
        "root_more":root_more,
        "error":error,
        "name":username,
    })

#详情
@csrf_exempt
def more(request,username,path):
    if(username=='username'):
        return  render(request,"login.html")
    from save.actionhdfs import show_more,get_all_file
    path=path.split("=")[1]
    try:
        error=0
        mess_list = get_all_file(path)
    except:
        error="路径不存在或者为文件!"
        mess_list=[]
    more_mess = show_more(path)
    return render(request,"index.html",{
        "error":error,
        "more":1,
        "name":username,
        "mess_list": mess_list,
        "path_value": path,
        "more_mess":more_mess,
    })
#删除目录
def delete(request,username,path):

    new_path = "/".join(path.split("/")[:-1])
    from save.actionhdfs import delete_path
    delete_path(path[5:])
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('path is')

    logger.info(path)
    logger.info(path[5:])
    os.system("hadoop fs -rm -r %s"%(path))
    delete_path(path)
    action1=""
    action1="delete  "+path
    Useraction.objects.create(username= username,action=action1)
    return file(request,username,new_path)

@csrf_exempt
#创建目录
def mkdir(request,username,path):
    # dataSource = request.POST.get("data_source")
    # print("-"*20)
    # print(dataSource)
    name = request.POST.get("mkdir") #用户提交的名字
    mk_path = path[5:] + "/" + name  #用来创建文件夹的名字
    from save.actionhdfs import mkdir_path
    if(mkdir_path(mk_path)):       #创建文件夹
        a=1
    else:a=2
    action1=""
    action1="make dircetion  "+mk_path
    #Useraction.objects.create(username= username,action=action1)
    #Useraction.objects.create(username= username,action="make dircetion"+mk_path)
    return file(request,username,path)

@csrf_exempt
#重命名文件
def rename(request,username,path):
    if(username=='level'):
        return  render(request,"login.html")
    name = request.POST.get("rename")  # 用户提交的名字
    rn_path = "/".join(path.split("/")[:-1])[5:] + "/" + name  # 用来重命名文件夹的名字
    from save.actionhdfs import rename_path
    rename_path(path[5:],rn_path)  # 重命名文件夹
    action1=""
    action1="rename  "+path+"  as  "+rn_path
    Useraction.objects.create(username= username,action=action1)
    return HttpResponseRedirect("/save/file/%s/%s" % (username,"/".join(path.split("/")[:-1])) )

#下载文件
@csrf_exempt
def down(request,username,path):
    name = request.POST.get("download") #用户提交的下载路径
    file_path = path[5:]  #文件在hdfs上的目录
    print(file_path)
    from save.actionhdfs import down_file
    # down_file(file_path,'/usr/hubingtest/')       #创建文件夹1处
    down_file(file_path,'/home/spark/dat/')
    action1=""
    # action1="download  "+file_path+" "+" to "+name
    Useraction.objects.create(username= username,action=action1)
    lenth=len(file_path)
    count=0
    string1=''
    string=file_path[::-1]
    for i in range(0,lenth):
        if string[i]=='/':
            string1=string[0:i]
            break
        i+=1
    string1=string1[::-1]
    # for i in range(0,lenth) :
    #     if file_path[i]=='/':
    #         count+=1
    #     if  count==3:
    #         break
    #     i+=1
    # for j in range(i,lenth):
    #      string1+=file_path[j]
    #      j+=1
    # open_path='/usr/hubingtest/'+string1 #第二处
    open_path='/home/spark/dat/'+string1
    file=open(open_path,'rb')
    # mm='/usr/hubingtest/胡兵model12321.py'.encode('utf-8').decode('ISO-8859-1')
    # file=open(mm,'rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="{}"'.format(string1).encode('utf-8').decode('ISO-8859-1')
    return response
    #return file(request,username,"/".join(path.split("/")[:-1]) )


#上传文件
@csrf_exempt
def upload(request,username,path):
    if(username=='level'):
        return  render(request,"login.html")
    # name = request.POST.get("up")  # 用户提交的上传文件路径
    username_file='username'
    content =request.FILES.get("upload", None)

    data_name=request.POST.get('data_name') # reverse
    print("**********" + data_name)
    data_source=request.POST.get('data_source') # reverse
    class_name=request.POST.get('class_name') # reverse
    important=request.POST.get('important') # reverse
    time=request.POST.get('time') # reverse
    place=request.POST.get('place') # reverse
    content_type="content"
    print(content_type)
    introduce="introduce"  # reverse
    logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(file_type)s - %(message)s')
    logger = logging.getLogger('file_type is')
    # logger.info(file_type)
    if not content:
      return HttpResponse("没有上传内容")
    print(path)
    file_path=path[5:]+"/"+content.name
    print(file_path)
    # file_record.objects.create(username=username_file,file_type=file_type,content_type=content_type,introduce=introduce,file_path=file_record_path)


    file_record.objects.create(file_name=content.name,data_name=data_name,data_source=data_source,\
                               class_name=class_name,important=important,time=time,place=place,file_path=file_path)

    # position = os.path.join('/usr/hubingtest',content.name)
    position = os.path.join('/home/spark/dat',content.name)
    print("position is: "+position)
    storage = open(position,'wb+')       #打开存储文件
    for chunk in content.chunks():       #分块写入文件
        storage.write(chunk)
    storage.close()                      #写入完成后关闭文件
    file_path = path[5:]  # 文件在hdfs上的目录
    print(content.name)

    # name="/usr/hubingtest/"+content.name
    name="/home/spark/dat/"+content.name
    print("name is :"+name)
    from save.actionhdfs import upload_file
    upload_file(file_path,name)       #创建文件夹
    action1=""
    action1="upload  "+file_path+name
    Useraction.objects.create(username= username,action=action1)
    #return HttpResponse("上传成功")      #返回客户端信息

    # file_path = path[5:]  # 文件在hdfs上的目录
    # from save.actionhdfs import upload_file
    # upload_file(file_path,name)       #创建文件夹
    # action1=""
    # action1="upload  "+file_path+name
    # Useraction.objects.create(username= username,action=action1)
    return file(request,username, path)

 # def read(request,username,path):
 #     print("如果不是目录显示该文件内容")


#上传文件夹
@csrf_exempt
def project(request):

    print("nihao")
    from save.actionhdfs import get_all_file
    #如果是用户提交查询
    if request.method == 'POST':

        data_name=request.POST.get('data_name')
        data_type=request.POST.get('data_type')
        important=request.POST.get('important')
        time=request.POST.get('time')
        place=request.POST.get('place')
        time_res=request.POST.get('time_res')
        space_res=request.POST.get('space_res')
        data_source=request.POST.get('data_source')
        direction=request.POST.get('direction')
        class_name=request.POST.get('direction')
        data_contact=request.POST.get('data_contact')
        contact_num=request.POST.get('contact_num')
        update_freq=request.POST.get('update_freq')
        data_desc=request.POST.get('data_desc')



        mkdir = request.POST.get("mkdir")
        print("-"*20)
        print(mkdir)
        path = request.POST.get("path")
        print("path is:")
        print(path)
        dir=request.FILES
        # print("dir is:"+dir)
        dirlist=dir.getlist('files')
        # print(dirlist)
        pathlist=request.POST.getlist('paths')#根据相对路径创建文件夹
        # print(dir)
        if not dirlist:
            return HttpResponse( 'files not found')
        else:
            for file in dirlist:
                # position = os.path.join(os.path.abspath(os.path.join(os.getcwd(),'/usr/hubingtest/')),'/'.join(pathlist[dirlist.index(file)].split('/')[:-1]))
                position = os.path.join(os.path.abspath(os.path.join(os.getcwd(),'/home/spark/dat/')),'/'.join(pathlist[dirlist.index(file)].split('/')[:-1]))
                if not os.path.exists(position):
                    os.makedirs(position )
                print("position2 is: "+position+'/'+file.name)
                storage = open(position+'/'+file.name, 'wb+')
                for chunk in file.chunks():
                    storage.write(chunk)
                storage.close()

                #分割

                c = position.split("/")
                length=len(c)
                i=0
                path1=path
                while(i<length):
                    sb=0
                    path1 = path1 +'/'+c[i]
                    from save.actionhdfs import get_all_file
                    if path1=="":
                        root_more=0
                    else:
                        root_more=1
                    try:
                        error=0
                        mess_list = get_all_file(path1)
                    except:
                        mess_list=[]
                        error="路径不存在或者为文件!"
                        sb=1
                    if(sb==1):#判断指定路径是否存在或者为文件
                        mk_path = path1 #用来创建文件夹的名字
                        from save.actionhdfs import mkdir_path
                        if(mkdir_path(mk_path)):       #创建文件夹mk_path = path[5:] + "/" + name 用来创建文件夹的名字
                            a=1
                        else:a=2
                    else:
                        pass
                    i=i+1


                name = position+'/'+file.name    #在服务器上local_path
                d = position[15:]     #代表的是去掉/usr/hubingtest  其中在hdfs上的文件路径
                file_path = path+'/'+d+'/'+file.name
                from save.actionhdfs import upload_file
                upload_file(file_path,name)
                file_record.objects.create(data_name=data_name,data_type=data_type,important=important,time=time,
                                           place=place,time_res=time_res,space_res=space_res,file_path=file_path,
                                           data_source=data_source,direction=direction,class_name=class_name,
                                           data_contact=data_contact,contact_num=contact_num,update_freq=update_freq,
                                           data_desc=data_desc)

                # file_path = path[5:] +position # 文件在hdfs上的目录
                # # name="/usr/hubingtest/"+content.name
                # name="E:\\test\\"+position
                # from save.actionhdfs import upload_file
                # upload_file(file_path,name)       #创建文件夹
            return HttpResponse( '成功')
    return HttpResponse("上传错误")

def search(request):
    username = request.COOKIES.get('username','level')
    print(username)
    if(username=='level'):
        return render(request,'login.html')
    data_name_list=[]
    data_source_list=[]
    class_name_list=[]
    important_list=[]
    time_list=[]
    place_list=[]

    #dataList = file_record.objects.filter(sa="WeizhongTu").filter(email="tuweizhong@163.com")


    data_name=file_record.objects.all().values('data_name')
    data_source=file_record.objects.all().values('data_source')
    class_name=file_record.objects.all().values('class_name')
    important=file_record.objects.all().values('important')
    times=file_record.objects.all().values('time')
    place=file_record.objects.all().values('place')

    for data in data_name:
        data_name_list.append(data['data_name'])

    for data_s in data_source:
        data_source_list.append(data_s["data_source"])

    for classs in class_name:
        class_name_list.append(classs['class_name'])

    for imports in important:
        important_list.append(imports["important"])

    for tim in times:
        time_list.append(tim["time"])

    for plac in place:
        place_list.append(plac["place"])

    return  render(request,'search.html',{"data_name_list":list(set(data_name_list)),"data_source_list":list(set(data_source_list)),"class_name_list":list(set(class_name_list)),\
                                        "important_list":list(set(important_list)),"time_list":list(set(time_list)),"place_list":list(set(place_list)) ,"username":username,'chooseIndex':'2' })

def answer(request):
    answer_list=[]

    data_name=request.POST.get("data_name")
    ret_data_name = data_name
    data_source=request.POST.get("data_source")
    ret_data_source = data_source
    class_name=request.POST.get("class_name")
    ret_class_name = class_name
    important=request.POST.get("important")
    ret_important = important
    time=request.POST.get("time")
    ret_time = time
    place=request.POST.get("place")
    ret_place = place


    answers=file_record.objects.all().values("file_path").filter(data_name=data_name,data_source=data_source,class_name=class_name,\
                                                                 important=important,time=time,place=place)
    for answer in answers:
        answer_list.append(answer["file_path"])


    data_name_list=[]
    data_source_list=[]
    class_name_list=[]
    important_list=[]
    time_list=[]
    place_list=[]
    data_name=file_record.objects.all().values('data_name')
    data_source=file_record.objects.all().values('data_source')
    class_name=file_record.objects.all().values('class_name')
    important=file_record.objects.all().values('important')
    times=file_record.objects.all().values('time')
    place=file_record.objects.all().values('place')
    #print(data_name +":"+ data_source +":"+ class_name +":"+ important +":"+ times +":"+ place)

    for data in data_name:
        data_name_list.append(data['data_name'])

    for data_s in data_source:
        data_source_list.append(data_s["data_source"])

    for classs in class_name:
        class_name_list.append(classs['class_name'])

    for imports in important:
        important_list.append(imports["important"])

    for tim in times:
        time_list.append(tim["time"])

    for plac in place:
        place_list.append(plac["place"])

    return render(request,'search.html',{'answer_list':list(set(answer_list)),"data_name_list":list(set(data_name_list)),"data_source_list":list(set(data_source_list)),"class_name_list":list(set(class_name_list)),\
                                        "important_list":list(set(important_list)),"time_list":list(set(time_list)),"place_list":list(set(place_list)),\
                                             "data_name":ret_data_name,"data_source":ret_data_source,"class_name":ret_class_name,\
                                             "important":ret_important,"time":ret_time,"place":ret_place},)

def function(request,function_name):
    print(function_name)
    # # username=username
    username = request.COOKIES.get('username','level')
    # print(username)
    if(username=='level'):
        return render(request,'login.html')
    # function_name = request.POST.get('gender1')       #function_class 分为五类方法，前端获取几种方法名称
    # # print(function)
    if function_name=="分类方法":
        v=1
    elif function_name == "单时间序列预测":
        v=2
    elif function_name == "关联分析":
        v=3
    elif function_name == "聚类方法":
        v=4
    else:
        v=5
    function_list=function_model.objects.all()
    function_list=function_model.objects.all().filter(function_class=v)
    # function_list=function_model.objects.all().filter(function_class=1)
    for functions in function_list:
        print(functions.introduce)
    return render(request,"function.html",{"function_list":function_list,"username":username,'chooseIndex':'4', "v":v})

def al(request):
    return render(request,"function_exec.html")


def function_exec(request):
    username = request.COOKIES.get('username','level')
    print(username)
    if(username=='level'):
        return render(request,'login.html')
    functions=function_model.objects.all().values("function_name")
    child_list=get_child_list("/kj_test")
    return render(request,"function_exec.html",{"functions":functions,"child_list":child_list,"username":username,'chooseIndex':'4'})

def function_exec(request, fname):
    username = request.COOKIES.get('username','level')
    # print("*"*20 + fname)
    functions=function_model.objects.all().values("function_name")
    child_list=get_child_list("/kj_test")
    return render(request,"function_exec.html",{"functions":functions,"child_list":child_list,"username":username,'fname':fname})










def function_count(request):
    parameter_string=""
    input_file=request.POST.get("function")
    #print ("*"*10 + input_file);
    input_file=function_model.objects.all().values("file_name").filter(function_name=input_file)
    input_file=input_file[0]
    input_file=input_file['file_name']

    print("input_file is :"+ input_file)
    input_path1=request.POST.get("input1")
    input_path2=request.POST.get("input2")
    output_path2=request.POST.get("output2")
    print("output2 is"+output_path2+"end")
    output_path1=request.POST.get("output1")
    parameter=request.POST.get("parameter")
    function_select=request.POST.get("function_select")
    # select=request._post.get("select")
    list_parameter=parameter.split(";")


    if function_select=="1":#深度学习的代码
        # down_file("",'/usr/hubingtest/')

       #10.27删除的 input_path1_temp="/kj/"+input_path1
        input_path1_temp="/kj/"+input_file#10.27添加的
  # down_file(input_path1_temp,'/usr/hubingtest/')
        down_file(input_path1_temp,'/home/spark/dat/')
        # input_path1="/usr/hubingtest/"+input_path1
        input_path1="/home/spark/dat/"+input_path1
        if input_path2==" ":
            pass
        else:
            input_path2_temp="/kj/"+input_path2
            # down_file(input_path2_temp,'/usr/hubingtest/')
            down_file(input_path2_temp,'/home/spark/dat/')
            # input_path2="/usr/hubingtest/"+input_path2
            input_path2="/home/spark/dat/"+input_path2
        if output_path1!=" ":
            # output_path1="/usr/hubingtest/"+output_path1
            output_path1="/home/spark/dat/"+output_path1
        if output_path2!="":
            # output_path2="/usr/hubingtest/"+output_path2
            output_path2="/home/spark/dat/"+output_path2
        python_string="nohup python2 "+"/home/spark/dat/"+input_file+" "+input_path1+" "+input_path2+" "+output_path1+" "+output_path2+" "+parameter_string[0:-1]
        print(python_string)
        print("start the count python")
        os.system(python_string)#执行python语句
        print("count is finished")
        upload_file("/kj/",output_path1)
        if output_path2!="":
            upload_file("/kj/",output_path2)
        return HttpResponse("success")
    else:
        input_path1="hdfs:///kj_test/"+input_path1
        input_file="/home/spark/dat/"+input_file 
        output_path1="hdfs:///kj_out/"+output_path1
        print("input_file: "+input_file)
        print("input_path1: "+input_path1)
        print("input_path2: "+input_path2)
        print("output_path1: "+output_path1)
        print("output_path2: "+output_path2)

        if(output_path2==" "):
            output_path2=output_path2
        else:
            output_path2="hdfs:///kj_out/"+output_path2
        if input_path2==" " or input_path2=="":
            input_path2=input_path2
        else:
            input_path2="hdfs:///kj_test/"+input_path2
        for par in list_parameter:
            parameter_string=parameter_string+par+" "
        print(input_file)
        print(input_path1)
        print(input_path2)
        print(output_path1)
        print(output_path2)
        print(list_parameter)
        print(parameter_string)
        # print(select)
        # spark_string=" spark-submit "+input_file+" "+input_path1+" "+input_path2+" "+output_path1+" "+output_path2+" "+parameter_string[0:-1]
        spark_string=" spark-submit "+input_file+" "+input_path1+" "+input_path2+" "+output_path1+" "+" "+parameter_string[0:-1]
        print(spark_string)
        os.system(spark_string)
        print("sucess2")
    # if select=="1":
    #     pass
    #     # os.system()
    # else:
    #     pass
   # output_path="temp9.png"
        if(function_select==1):
            output_path=output_path1
        else:
            output_path=" "
    return render(request,"answer_view.html",{"image_name":output_path})















def function_upload(request):
    content =request.FILES.get("upload", None)
    file_name=content.name
    function_name=request.POST.get("function_name")
    function_type=request.POST.get("function_type")
    upload_user=request.POST.get("upload_user")
    input_files_path=request.POST.get("input_files_path")
    output_files_path=request.POST.get("output_files_path")
    parameter=request.POST.get("parameter")
    introduce=request.POST.get("introduce")

    # if os.path.exists("/usr/hubingtest"):
    if os.path.exists("/home/spark/dat"):
        pass
    else:
        # os.mkdir("/usr/hubingtest")
        os.mkdir("/home/spark/dat")

    # position = os.path.join('/usr/hubingtest/',content.name)
    position = os.path.join('/home/spark/dat/',content.name)
    storage = open(position,'wb+')       #打开存储文件
    for chunk in content.chunks():       #分块写入文件
        storage.write(chunk)
    storage.close()
    print(position)
    upload_file('/kj',position)
    function_model.objects.create(function_name=function_name,file_name=file_name,function_type=function_type,upload_user=upload_user,\
                                  input_files_path=input_files_path,output_files_path=output_files_path,parameter=parameter,\
                                  introduce=introduce)

    return HttpResponse("success")

def function_search(request):
    username = request.COOKIES.get('username','level')
    print(username)
    if(username=='level'):
        return render(request,'login.html')
    function_type_list=function_model.objects.all().values("function_type")
    upload_user_list=function_model.objects.all().values("upload_user")
    return render(request,"function_search.html",{"function_type_list":function_type_list,"upload_user_list":upload_user_list,"username":username,"chooseIndex": "5"})

def function_answer(request):
    function_type=request.POST.get("function_type")
    upload_user=request.POST.get("upload_user")
    function_list=function_model.objects.all().filter(function_type=function_type,upload_user=upload_user)
    for functions in function_list:
        print(functions.introduce)
    return render(request,"function.html",{"function_list":function_list})



def image_show(request,imagename):
    imagename="/media/mypicture/"+imagename
    return render(request,"answer_view.html",{"imagename":imagename})

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
#from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from online.models import  User,Userlogin,Permission,Role


#表单
#@csrf_protect
class UserFormLogin(forms.Form):
    username = forms.CharField(label='名称',widget=forms.TextInput(attrs={'width':'400px'}))
    password = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'width':'270px'}))
    # password=forms.PasswordInput()
# class UserFormLogin(forms.Form):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField()

class UserForm(forms.Form):
    username = forms.CharField(label='名称',)
    # password1 = forms.PasswordInput(label=' 密码',
    # password2 = forms.PasswordInput(label='确认密码',)
    password1 = forms.CharField(label='密码',widget=forms.PasswordInput())
    password2 = forms.CharField(label='密码',widget=forms.PasswordInput)
    email = forms.CharField(label='邮箱',widget=forms.EmailInput())
    employer=forms.CharField(label='工作单位')
    tel=forms.CharField(label='联系方式')


#注册
def regist(req):
    if req.method == 'POST':
        # uf = UserForm(req.POST)
        # if uf.is_valid():
            #获得表单数据
        username = req.POST.get('username')
        filter_result=User.objects.filter(username=username)
        if len(filter_result)>0 :
            return HttpResponse("用户名已经存在")
        password1 =req.POST.get('pwd1')
        password2 = req.POST.get('pwd2')
        email = req.POST.get('email')
        employer=req.POST.get('employer')
        tel=req.POST.get("tel")

        #添加到数据库
        if password1==password2:
           User.objects.create(username= username,password=password1,email=email,employer=employer,tel=tel)
        else: return HttpResponse("两次密码输入不一致")
        #return render(req,'share.html')
        return render(req, 'share.html')
    # else:
        # uf = UserForm()
    #return render(req,'regist.html')
    return render(req, 'regist.html')

#登陆
def login(req):
    if req.method == 'POST':
        username=req.POST.get("username")
        password=req.POST.get("pwd")
        username = username.strip()
        password = password.strip()
        if(username=='level'):
            #return render(req,'login.html')
            return render(req, 'login.html')

        user = User.objects.filter(username__exact = username,password__exact = password)
        if user:
            #比较成功，跳转index
            # print(username)
            # print(req.session['username'])
            # req.session['username']=username

            response = HttpResponseRedirect('/online/index/')
            #将username写入浏览器cookie,失效时间为3600
            response.set_cookie('username',username,3600)

            #竟然在这里写十几个cookies!!
            user_ = User.objects.get(username=username, password= password)
            permission = user_.role.permission
            response.set_cookie('wenjianziyuan', permission.wenjianziyuan, 3600)
            response.set_cookie('hbaseshujuku', permission.hbaseshujuku, 3600)
            response.set_cookie('moxingsuanfa', permission.moxingsuanfa, 3600)
            response.set_cookie('ziyuanguanli', permission.ziyuanguanli, 3600)
            response.set_cookie('ziyuanchaxun', permission.ziyuanchaxun, 3600)
            response.set_cookie('suanfaziyuan', permission.suanfaziyuan, 3600)
            response.set_cookie('moxingziyuan', permission.moxingziyuan, 3600)
            response.set_cookie('suanfachaxun', permission.suanfachaxun, 3600)
            response.set_cookie('yanshi', permission.yanshi, 3600)
            response.set_cookie('tijao', permission.tijao, 3600)
            response.set_cookie('shujuku', permission.shujuku, 3600)

            print("wenjianziyuan" +permission.wenjianziyuan)
            print("hbaseshujuku" +permission.hbaseshujuku)
            print("ziyuanguanli" +permission.ziyuanguanli)

            Userlogin.objects.create(username= username)
            return response
        else:
            # 比较失败，还在login
            return HttpResponseRedirect('/online/login/')
                 #return render(req,'login.html',{"errors":"用户名已存在"})
    # else:
    #
    #     uf = UserFormLogin()
    #return render(req,'login.html')
    return render(req,'login.html')

import json
def checkusername(req):
    name = req.POST.get("name", None)
    print('已经进行到检查用户名的阶段了' + name)
    if name is not None: 
        user = User.objects.filter(username__exact = name)
        if user:
            return HttpResponse(json.dumps({"msg":"true"}))
    return HttpResponse(json.dumps({"msg":"false"}))

def checkpwd(req):
    name = req.POST.get("name", None)
    pwd = req.POST.get("pwd", None)
    if name is not None:
        user = User.objects.filter(username__exact = name,password__exact = pwd)
        if user:
            return HttpResponse(json.dumps({"msg":"true"}))
    return HttpResponse(json.dumps({"msg":"false"}))

#登陆成功
def index(req):
    username = req.COOKIES.get('username','level')
    print(username)
    if(username=='level'):
        #return render(req,'login.html')
        return render(req,'login.html')
    return render(req,'firstpage.html', {'username':username, 'chooseIndex':'0', 'file_code': 'file_0'})

def index1(req):
    username = req.COOKIES.get('username','level')
    print(username)
    if(username=='level'):
        return render(req,'login.html')
    return render(req,'firstpage0.html', {'username':username, 'chooseIndex':'0', 'file_code': 'file_0'})


#退出
def logout(req):
    response = HttpResponse('logout !!')
    #清理cookie里保存username
    response.delete_cookie('username')
    return render(req,'logout.html')



#用户管理页面
def usercrm(req):
    if req.method=="POST":
        if 'id' in req.POST: ## 修改表单提交过来的
            id = req.POST.get('id')
            modifyuser = User.objects.get(pk = id)
            modifyuser.username  = req.POST.get('usename')
            modifyuser.password = req.POST.get('password')
            # 外键的保存
            modifyrole = Role.objects.get(id = req.POST.get('rolename'))
            modifyuser.role = modifyrole
            modifyuser.save() # 保存
        else:# 新增用户表单过来的
            username = req.POST.get('username')
            filter_result=User.objects.filter(username=username)
            if len(filter_result)>0 :
                #return HttpResponse("用户名已经存在")
                return render(req,'useradd.html', {"message": "用户名已经存在"})
            password1 =req.POST.get('pwd1')
            password2 = req.POST.get('pwd2')
            email = req.POST.get('email')
            employer=req.POST.get('employer')
            tel=req.POST.get("tel")
            #roleid = req.POST.get("roleid")
            role = Role.objects.get(id = req.POST.get('roleid'))

            #添加到数据库
            if password1==password2:
                User.objects.create(username= username,password=password1,email=email,employer=employer,tel=tel,role=role)
            else:
                #return HttpResponse("两次密码输入不一致")
                return render(req,'useradd.html', {"message": "两次密码输入不一致"})
    if 'type' in req.GET:
        type = req.GET.get('type')
        pid = req.GET.get('id')
        import re
        if(type == 'modify'): # 修改
            userdetail = User.objects.get(pk = re.sub("\D", "", pid))
            rolelist = Role.objects.all()
            return render(req,'userdetail.html', {'userdetail': userdetail, 'rolelist':rolelist})
        elif(type == 'delete'):  # 删除
            deleteuser = User.objects.get(pk = re.sub("\D", "", pid))
            deleteuser.delete()
        elif(type == 'add'):     #新增用户
            rolelist = Role.objects.all()
            return render(req,'useradd.html',{'rolelist':rolelist})

    userlist = User.objects.all()
    return render(req,'usercrm.html', {'userlist' : userlist})

def ajax(req):
    roleid = req.POST.get('roleid')
    role = Role.objects.get(pk = roleid)
    return HttpResponse(role.permission.name)

def rolecrm(req):
    if req.method=="POST":
        if 'id' in req.POST: ## 修改表单提交过来的
            id = req.POST.get('id')
            modifyrole = Role.objects.get(pk = id)
            modifyrole.rolename  = req.POST.get('rolename')
            # 外键的保存
            modifyper = Permission.objects.get(id = req.POST.get('permissionid'))
            modifyrole.permission = modifyper
            modifyrole.save() # 保存
        else: #新增角色表单过来的
            rolename = req.POST.get('rolename')
            filter_result=Role.objects.filter(rolename=rolename)
            if len(filter_result)>0 :
                return render(req,'roleadd.html', {"message": "角色名称已经存在"})
            permission = Permission.objects.get(id = req.POST.get('permissionid'))
            Role.objects.create(rolename= rolename,permission=permission)
    if 'type' in req.GET:
        type = req.GET.get('type')
        pid = req.GET.get('id')
        import re
        if(type == 'modify'): # 修改
            permissionlist = Permission.objects.all()
            roledetail = Role.objects.get(pk = re.sub("\D", "", pid))
            return render(req,'roledetail.html', {'roledetail': roledetail, 'permissionlist': permissionlist})
        elif(type == 'delete'):  # 删除
            deleterole = Role.objects.get(pk = re.sub("\D", "", pid))
            deleterole.delete()
        elif(type == 'add'):     #新增用户
            permissionlist = Permission.objects.all()
            return render(req,'roleadd.html', {'permissionlist': permissionlist})

    rolelist = Role.objects.all()
    return render(req,'rolecrm.html',{'rolelist':rolelist})

def permissioncrm(req):
    if req.method == "POST":
        if 'id' in req.POST:
            id = req.POST.get('id')
            if id != '':         ## 修改表单提交过来的
                modifypermission = Permission.objects.get(pk = id)
                modifypermission.name = req.POST.get('name')
                modifypermission.wenjianziyuan = req.POST.get('wenjianziyuan')
                modifypermission.hbaseshujuku = req.POST.get('hbaseshujuku')
                modifypermission.moxingsuanfa = req.POST.get('moxingsuanfa')
                # modifypermission.shouye = req.POST.get('shouye')

                modifypermission.ziyuanguanli = req.POST.get('ziyuanguanli')
                modifypermission.ziyuanchaxun = req.POST.get('ziyuanchaxun')
                modifypermission.jiqunchakan = req.POST.get('jiqunchakan')
                modifypermission.suanfaziyuan = req.POST.get('suanfaziyuan')
                modifypermission.moxingziyuan = req.POST.get('moxingziyuan')

                modifypermission.suanfachaxun = req.POST.get('suanfachaxun')
                modifypermission.yanshi = req.POST.get('yanshi')
                modifypermission.tijao = req.POST.get('tijao')
                modifypermission.shujuku = req.POST.get('shujuku')
                modifypermission.save() # 保存
            else:  # 新增权限表过来的
                name = req.POST.get('name')
                filter_result = Permission.objects.filter(name = name)
                if len(filter_result) > 0 :
                    return render(req, 'permissiondetail.html', {"message": "权限名称已经存在"})
                permission = Permission.objects.create(name = name)
                permission.wenjianziyuan = req.POST.get('wenjianziyuan')
                permission.hbaseshujuku = req.POST.get('hbaseshujuku')
                permission.moxingsuanfa = req.POST.get('moxingsuanfa')
                # modifypermission.shouye = req.POST.get('shouye')

                permission.ziyuanguanli = req.POST.get('ziyuanguanli')
                permission.ziyuanchaxun = req.POST.get('ziyuanchaxun')
                permission.jiqunchakan = req.POST.get('jiqunchakan')
                permission.suanfaziyuan = req.POST.get('suanfaziyuan')
                permission.moxingziyuan = req.POST.get('moxingziyuan')

                permission.suanfachaxun = req.POST.get('suanfachaxun')
                permission.yanshi = req.POST.get('yanshi')
                permission.tijao = req.POST.get('tijao')
                permission.shujuku = req.POST.get('shujuku')
                permission.save() # 保存

    if 'type' in req.GET:
        type = req.GET.get('type')
        pid = req.GET.get('id')
        import re
        if(type == 'modify'): # 修改
            permissiondetail = Permission.objects.get(pk = re.sub("\D", "", pid))
            return render(req,'permissiondetail.html', {'permissiondetail': permissiondetail})
        elif(type == 'delete'):  # 删除
            deletepermission = Permission.objects.get(pk = re.sub("\D", "", pid))
            deletepermission.delete()
        elif(type == 'add'):     #新增角色
            return render(req,'permissionadd.html')

    permissionlist = Permission.objects.all()
    return render(req,'permissioncrm.html', {'permissionlist': permissionlist})
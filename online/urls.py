from django.conf.urls import url,include
from django.contrib import admin
from online import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^regist/$',views.regist,name = 'regist'),
    url(r'^index/$',views.index,name = 'index'),
    url(r'^index1/$',views.index1,name = 'index1'),
    url(r'^logout/$',views.logout,name = 'logout'),

    url(r'^checkusername/$',views.checkusername,name = 'checkusername'),
    url(r'^checkpwd/$',views.checkpwd,name = 'checkpwd'),
    url(r'^usercrm/$',views.usercrm,name = 'usercrm'),
    url(r'^ajax/$',views.ajax,name = 'ajax'),
    url(r'^rolecrm/$',views.rolecrm,name = 'rolecrm'),
    url(r'^permissioncrm/$',views.permissioncrm,name = 'permissioncrm'),


]
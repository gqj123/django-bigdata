"""django_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from online.views import *
from save.views import *
from django.conf.urls.static import  static
from django.conf import settings
from student import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^online/', include('online.urls')),
    url(r"^", include('online.urls')),
    url(r'^save/', include("save.urls")),
    url(r'^search/',search),
    url(r'^answer/',answer),
    url(r'^updatesystem/$',views.updatesystem,name='updatesystem'),
    url(r'^getipaddr/$',views.getipaddr,name='getipaddr'),
    url(r'^getipaddr1/$',views.getipaddr1,name='getipaddr1'),
    url(r'^getipaddr2/$',views.getipaddr2,name='getipaddr2'),
    url(r'^getipaddr3/$',views.getipaddr3,name='getipaddr3'),
    url(r'^getipaddr4/$',views.getipaddr4,name='getipaddr4'),
    url(r'^getipaddr5/$',views.getipaddr5,name='getipaddr5'),
    url(r'^addpath/$',views.addpath,name='addpath'),
    url(r'^getipaddr5/$',views.getipaddr5,name='getipaddr5'),
    url(r'^project/$',project,name='project'),

    #url(r'^hbasecheck/$',views.hbasecheck,name='hbasecheck'),
    url(r'^hbaseTable/(.+)/$',views.hbaseTable,name='hbaseTable'),

    url(r'^filedata/(.+)/$',views.filedata,name='filedata'),

    url(r'^sparkcheck/$',views.sparkcheck,name='sparkcheck'),

    url(r'^testhdfs/$',views.testhdfs,name='testhdfs'),

    url(r'^downhdfs/$',views.downhdfs,name='downhdfs'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

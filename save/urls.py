from django.conf.urls import url

from save.views import *

from django.conf.urls.static import  static
from django.conf import settings

urlpatterns = [
    url(r'^hdfsfile/(\w+)/$', hdfsfile),
    url(r'^more/(\w+)/(.+)/$', more),
    url(r'^file/(\w+)/(.+)/$', file),
    url(r'^delete/(\w+)/(.+)/$', delete),
    url(r'^mkdir/(\w+)/(.+)/$', mkdir),
    url(r'^rename/(\w+)/(.+)/$', rename),
    url(r'^down/(\w+)/(.+)/$', down),
    url(r'^upload/(\w+)/(.+)/$', upload),
    url(r'^search/$',search,name='search'),
    url(r'^answer/$',answer,name='answer'),
    url(r'^al/$',al,name='al'),

    url(r'^function/(.+)/$',function,name='function'),

    url(r'^function_upload/$',function_upload,name='function_load'),
    url(r'^function_exec/$',function_exec,name='function_exec'),
    url(r'^function_exec/(.+)$',function_exec,name='function_exec'),

    url(r'^function_search/$',function_search,name='function_search'),
    url(r'^function_count/$',function_count,name='function_count'),
    url(r'^function_answer/$',function_answer,name='function_answer'),
    url(r'^image_show/(.+)/$', image_show,name="image_show"),
#



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

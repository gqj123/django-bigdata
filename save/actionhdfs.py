# -*- coding: utf-8 -*-
from hdfs import *
import os
import time
# connect hdfs
def connect():
    #client = Client("http://192.168.168.228:50070",)
    # client = Client("http://202.199.10.22:50070",root="/",timeout=1000,session=False)
    client = Client("http://221.239.0.181:50070",root="/",timeout=1000,session=False)
    return client
#将字典转化为类
def dict2obj(args):
    '把字典递归转化为类'
    class obj(object):
        def __init__(self, d):
            for a, b in d.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, obj(b) if isinstance(b, dict) else b)
    return obj(args)

#get all file
def get_all_file(path):
    client = connect()
    mess_list = []
    if path=="/":
        pass
    else:
        path=path+"/"
    child_list = client.list(path)
    for child in child_list:
        one_dic = client.status(path+child)
        filepath = path+child
        one_dic["path"]=filepath
        one_dic["path1"]=child

        dict2obj(one_dic)
        # 修改时间1528353247347,13位到毫秒，需要转化为10位到秒的时间戳（需要是float类型）
        modify_time = dict2obj(one_dic).modificationTime/1000.0
        # 使用localtime()和格式化输出strftime()将时间戳转化为普通的格式
        modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modify_time))
        one_dic["modificationTime"] = modify_time
        # print(dict2obj(one_dic).modificationTime)
        length =StrOfSize(dict2obj(one_dic).length)
        one_dic["length"] = length
        print(one_dic["path"])
        mess_list.append(dict2obj(one_dic))
    return mess_list


def get_hdfs_file(path):
    print('你不会迷路了吧' + path)
    client = connect()
    mess_list = []
    if path=="/":
        pass
    else:
        # path=path+"/"
        path = path
    index = 0
    # for root, dir, files in client.walk(path, status=True):
    #     if index == 0:
    #         index += 1
    #         continue
    #
    #     print(root)
    #
    #     # //print(dir[0]),print('*'*20)
    #     for childroot, childdir, childfiles in client.walk(root[0] + '/', status=True):
    #
    #         for file in childfiles:
    #             dict = {}
    #             print(childroot)
    #             print(file)
    #
    #             dict['filename'] = file[0]
    #             dict['filepath'] = childroot[0] +'/' + file[0]
    #             time = filter(str.isdigit, file[0])
    #             dict['filetime'] = ''.join(list(time))
    #             mess_list.append(dict)

    for root, dir, files in client.walk(path, status=True):
        for file in files:
            dict = {}
            # allfile.append(root[0] + '/' + file[0])
            dict['filename'] = file[0]
            dict['filepath'] = root[0] + '/' + file[0]
            time = filter(str.isdigit, file[0])
            dict['filetime'] = ''.join(list(time))
            mess_list.append(dict)
    print(mess_list)
    return mess_list





#修改文件尺寸大小
def StrOfSize(size):
    '''
    递归实现，精确为最大单位值 + 小数点后三位
    '''
    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level+1 > len(units):
        level = -1
    return ( '{}.{:>02d} {}'.format(integer, remainder, units[level]) )
def get_child_list(path):
    client=connect()
    child_list=[]
    child_list=client.list(path)
    return child_list
#more
def show_more(path):
    client = connect()
    return client.status(path)
#delete
def delete_path(path):
    client = connect()
    return client.delete(path,recursive=True)

#makedirs
def mkdir_path(path):
    client = connect()
    return client.makedirs(path)

#重命名
def rename_path(old_path,new_path):
    client = connect()
    return client.rename(old_path,new_path)

#下载文件
def down_file(hdfs_path,local_path):
    client = connect()
    return client.download(hdfs_path,local_path,overwrite=True)

#上传文件
def upload_file(hdfs_path,local_path):
    client = connect()
    return client.upload(hdfs_path,local_path,overwrite=True)

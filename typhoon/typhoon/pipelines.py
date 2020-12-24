# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.exceptions import DropItem

class TyphoonPipeline(object):
    # def process_item(self, item, spider):
    #     return item

    # def printitems(self, item):
    #     print(item)

    def process_item(self, item, spider):
        flag = 0
        folder = os.path.exists(item['located'] + '\\' + item['name']+'\\'+item['thistime'])
        if not folder:
            os.makedirs(item['located'] + '\\' + item['name']+'\\'+item['thistime'])
        filename = item['located'] + '\\' + item['name'] + '\\' + item['thistime'] + '\\' + item['country'] + '.txt'
        open(filename, 'a')
        for line in open(filename):
            if ('时间：' + item['time'] + '  '+'中心位置：' + item['place'] + '  '+'中心气压：' + item['pressure'] + '  '+'最大风速：' + item['speed'] + '  '+'风力：' + item['power'] + '\n') == line:
                flag = 1
                break
        if flag == 1:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            with open(filename, 'a') as f:
                f.write('时间：' + item['time'] + '  ')
                f.write('中心位置：' + item['place'] + '  ')
                f.write('中心气压：' + item['pressure'] + '  ')
                f.write('最大风速：' + item['speed'] + '  ')
                f.write('风力：' + item['power'] + '\n')
            return item



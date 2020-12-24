# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from typhoon.items import TyphoonItem

class TyspiderSpider(scrapy.Spider):
    name = 'tySpider'
    allowed_domains = ['typhoon.zjwater.gov.cn']
    start_urls = ['http://typhoon.zjwater.gov.cn/Api/TyhoonActivity']

    def __init__(self, located=None, *args, **kwargs):
        super(TyspiderSpider, self).__init__(*args, **kwargs)
        self.located=located

    def parse(self, response):
        tfids = response.xpath('//tfid/text()').extract()
        names = response.xpath('//name/text()').extract()
        timeformates = response.xpath('//timeformate/text()').extract()
        tflist = []
        for n in range(len(tfids)):
            tflist.append([tfids[n], names[n], timeformates[n]])
        for m in range(len(tflist)):
            url = 'http://typhoon.zjwater.gov.cn/Api/TyphoonInfo/' + tflist[m][0]
            # yield scrapy.Request(url, callback=self.parse_detail)
            yield scrapy.Request(url, callback=lambda response, name=tflist[m][1],timeformate=tflist[m][2]: self.parse_detail(response, name,timeformate))



    def parse_detail(self, response,name,timeformate):
        #添加实际点
        need1 = response.xpath('//typhoonpointmodel').extract()[-1]
        soup00 = BeautifulSoup(need1, 'lxml')
        item = TyphoonItem()
        item['located'] = self.located
        item['thistime'] = timeformate
        item['name'] = name
        item['place'] = soup00.lng.text + '°/' + soup00.lat.text + '°'
        item['time'] = soup00.time.text
        item['speed'] = soup00.speed.text + '米/秒'
        item['country'] = "观测值"
        item['pressure'] = soup00.pressure.text + '百帕'
        item['power'] = soup00.power.text + '级'
        yield item

        #添加预测点
        need = response.xpath('//forecast').extract()[-1]
        soup0 = BeautifulSoup(need, 'lxml')
        forecastmodels = soup0.find_all('forecastmodel')
        for forecastmodel in forecastmodels:
            soup1 = BeautifulSoup(str(forecastmodel), 'lxml')
            tm = soup1.tm.text
            pointmodels = soup1.find_all('pointmodel')
            pointmodel = pointmodels[0]
            print()
            for pointmodel in pointmodels[1:]:
                item = TyphoonItem()
                item['located'] = self.located
                item['thistime'] = timeformate
                item['name'] = name
                item['country'] = tm
                soup2 = BeautifulSoup(str(pointmodel), 'lxml')
                item['time'] = soup2.time.text
                item['place'] = soup2.lng.text + '°/' + soup2.lat.text + '°'
                item['pressure'] = soup2.pressure.text + '百帕'
                item['speed'] = soup2.speed.text + '米/秒'
                item['power'] = soup2.power.text + '级'
                yield item



#!/usr/bin/python
# coding=utf-8

import json

import scrapy
from scrapy.cmdline import execute

from autohome.items import SeriesItem
from autohome.spiders.utils.DbUtils import DbUtils
from autohome.spiders.utils.ExcelUtils import ExcelUtils


class SeriesSpider(scrapy.Spider):
    name = 'config_3_series'

    def __init__(self):
        # 数据库操作
        dbUtils = DbUtils('config_1_brand')
        self.queryItems = dbUtils.select(None)

    def start_requests(self):
        for item in self.queryItems:
            url = 'https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=3&value=%s' % item['_id']
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        responseBody = response.body.decode(response.encoding)
        factoryItems = json.loads(responseBody)['result']['factoryitems']
        for factoryItem in factoryItems:
            for item in factoryItem['seriesitems']:
                seriesItem = SeriesItem()
                seriesItem['id'] = item['id']
                seriesItem['name'] = item['name']
                seriesItem['firstLetter'] = item['firstletter']
                seriesItem['seriesState'] = item['seriesstate']
                seriesItem['seriesOrder'] = item['seriesorder']
                seriesItem['parentId'] = factoryItem['id']
                yield seriesItem


if __name__ == "__main__":
    execute(['scrapy', 'crawl', 'config_3_series'])
    dbUtils = DbUtils('config_3_series')
    queryItems = dbUtils.select(None)
    excelUtils = ExcelUtils()
    excelUtils.generateExcel('config', 'config_3_series', list(queryItems))

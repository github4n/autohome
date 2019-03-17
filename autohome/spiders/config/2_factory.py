#!/usr/bin/python
# coding=utf-8

import json

import scrapy
from scrapy.cmdline import execute

from autohome.items import FactoryItem
from autohome.spiders.utils.DbUtils import DbUtils


class FactorySpider(scrapy.Spider):
    name = '2_factory'

    def __init__(self):
        # 数据库操作
        dbUtils = DbUtils('1_brand')
        self.queryItems = dbUtils.select(None)

    def start_requests(self):
        for item in self.queryItems:
            url = 'https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=3&value=%s' % item['_id']
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        parentId = str(response.url).strip().split("value=")[-1]
        responseBody = response.body.decode(response.encoding)
        factoryItems = json.loads(responseBody)['result']['factoryitems']
        for item in factoryItems:
            factoryItem = FactoryItem()
            factoryItem['id'] = item['id']
            factoryItem['name'] = item['name']
            factoryItem['firstLetter'] = item['firstletter']
            factoryItem['parentId'] = parentId
            yield factoryItem


if __name__ == "__main__":
    execute(['scrapy', 'crawl', '2_factory'])

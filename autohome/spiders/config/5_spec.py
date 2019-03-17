#!/usr/bin/python
# coding=utf-8

import json

import scrapy
from scrapy.cmdline import execute

from autohome.items import YearItem
from autohome.spiders.utils.DbUtils import DbUtils


class SpecSpider(scrapy.Spider):
    name = '5_spec'

    def __init__(self):
        # 数据库操作
        dbUtils = DbUtils('3_series')
        self.queryItems = dbUtils.select(None)

    def start_requests(self):
        for item in self.queryItems:
            url = 'https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=5&value=%s' % item['id']
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        responseBody = response.body.decode(response.encoding)
        yearItems = json.loads(responseBody)['result']['yearitems']
        for yearItem in yearItems:
            for item in yearItem['specitems']:
                resultItem = YearItem()
                resultItem['id'] = item['id']
                resultItem['name'] = item['name']
                resultItem['parentId'] = yearItem['id']
                yield resultItem


if __name__ == "__main__":
    execute(['scrapy', 'crawl', '5_spec'])

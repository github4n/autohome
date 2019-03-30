#!/usr/bin/python
# coding=utf-8

import json

import scrapy
from scrapy.cmdline import execute

from autohome.items import YearItem
from autohome.spiders.utils.DbUtils import DbUtils
from autohome.spiders.utils.ExcelUtils import ExcelUtils


class SpecSpider(scrapy.Spider):
    name = 'config_5_spec'

    def __init__(self):
        # 数据库操作
        dbUtils = DbUtils('config_3_series')
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
    execute(['scrapy', 'crawl', 'config_5_spec'])
    dbUtils = DbUtils('config_5_spec')
    queryItems = dbUtils.select(None)
    excelUtils = ExcelUtils()
    excelUtils.generateExcel('config', 'config_5_spec', list(queryItems))

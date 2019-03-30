#!/usr/bin/python
# coding=utf-8

import json

import scrapy
from scrapy.cmdline import execute

from autohome.items import YearItem
from autohome.spiders.utils.DbUtils import DbUtils
from autohome.spiders.utils.ExcelUtils import ExcelUtils


class YearSpider(scrapy.Spider):
    name = 'config_4_year'

    def __init__(self):
        # 数据库操作
        dbUtils = DbUtils('config_3_series')
        self.queryItems = dbUtils.select(None)

    def start_requests(self):
        for item in self.queryItems:
            url = 'https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=5&value=%s' % item['id']
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        parentId = str(response.url).strip().split("value=")[-1]
        responseBody = response.body.decode(response.encoding)
        yearItems = json.loads(responseBody)['result']['yearitems']
        for item in yearItems:
            yearItem = YearItem()
            yearItem['id'] = item['id']
            yearItem['name'] = item['name']
            yearItem['parentId'] = parentId
            yield yearItem


if __name__ == "__main__":
    execute(['scrapy', 'crawl', 'config_4_year'])
    dbUtils = DbUtils('config_4_year')
    queryItems = dbUtils.select(None)
    excelUtils = ExcelUtils()
    excelUtils.generateExcel('config', 'config_4_year', list(queryItems))

#!/usr/bin/python
# coding=utf-8

import json

import scrapy
from scrapy.cmdline import execute
from autohome.items import BrandItem
from autohome.spiders.utils.DbUtils import DbUtils
from autohome.spiders.utils.ExcelUtils import ExcelUtils


class BrandSpider(scrapy.Spider):
    name = 'config_1_brand'
    start_urls = ['https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=1']

    def parse(self, response):
        responseBody = response.body.decode(response.encoding)
        brandItems = json.loads(responseBody)['result']['branditems']
        for item in brandItems:
            brandItem = BrandItem()
            brandItem['_id'] = item['id']
            brandItem['name'] = item['name']
            brandItem['bfirstletter'] = item['bfirstletter']
            brandItem['logo'] = item['logo']
            yield brandItem


if __name__ == "__main__":
    execute(['scrapy', 'crawl', 'config_1_brand'])
    dbUtils = DbUtils('config_1_brand')
    queryItems = dbUtils.select(None)
    excelUtils = ExcelUtils()
    excelUtils.generateExcel('config', 'config_1_brand', list(queryItems))

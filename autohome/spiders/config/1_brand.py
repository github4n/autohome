#!/usr/bin/python
# coding=utf-8

import json

import scrapy
from scrapy.cmdline import execute
from autohome.items import BrandItem


class BrandSpider(scrapy.Spider):
    name = '1_brand'
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
    execute(['scrapy', 'crawl', '1_brand'])

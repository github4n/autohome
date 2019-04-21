#!/usr/bin/python
# coding=utf-8
import os
import re

import scrapy
from scrapy.cmdline import execute

from autohome.spiders.utils.DbUtils import DbUtils
from autohome.spiders.utils.PathUtils import PathUtils


# 主要爬取series的车身外观
class SeriesImgsSpider(scrapy.Spider):
    name = 'SeriesBodySpider'
    # 当前项目根目录
    rootPath = PathUtils.getRootPath()

    def __init__(self):
        PathUtils.initDir()  # 创建目录
        # 数据库操作
        dbUtils = DbUtils('config_3_series')
        # self.queryItems = dbUtils.select({"id": 511})
        # self.queryItems = dbUtils.select(None)
        self.queryItems = dbUtils.selectByPage(None, 0, 1)

    # 初始请求
    def start_requests(self):
        for item in self.queryItems:
            url = 'https://car.autohome.com.cn/pic/series/%s-1.html' % item['id']
            PathUtils.createDir(self.rootPath + '/output//picture/' + item['name'])
            PathUtils.createDir(self.rootPath + '/output//picture/' + item['name']+'/车身外观')  # 创建目录
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        responseBody = response.body.decode(response.encoding)

        # 提取分页信息
        pageUrls = re.findall('/pic/series/\d{0,4}\W1-p\d{1,3}.html', responseBody)
        for pageUrl in pageUrls:
            pageUrl = "https://car.autohome.com.cn/" + pageUrl
            yield scrapy.http.Request(url=pageUrl, callback=self.parse)

        # 提取图片详情
        carName = response.xpath("/html/body/div[2]/div/div[2]/div[7]/div/div[1]/h2/a/text()").extract()[0]  # 提取车的名字
        img_urls = re.findall(r'<a href="/photo/series/(.*?)"', responseBody)  # 提取url
        img_urls = list(map(self.fullUrl, img_urls))  # 拼接成完整的url
        for url in img_urls:
            yield scrapy.http.Request(url=url, meta={'carName': carName}, callback=self.getImage)

    # 提取高清大图url
    def getImage(self, response):
        img_url = re.search(r'<img id="img" src="(.*?)"', response.text).group(1)
        img_url = "https:" + img_url
        carName = response.meta['carName']
        yield scrapy.http.Request(url=img_url, meta={'carName': carName}, callback=self.saveImage)

    # 保存大图片
    def saveImage(self, response):
        carName = response.meta['carName']
        fileName = response.url.split('/')[-1]
        rootPath = PathUtils.getRootPath()
        with open("%s/output/picture/%s/车身外观/%s" % (rootPath, carName, fileName), 'wb') as f:
            f.write(response.body)

    # 构建完整url
    def fullUrl(self, x):
        return 'https://car.autohome.com.cn/photo/series/' + x


if __name__ == "__main__":
    execute(['scrapy', 'crawl', 'SeriesBodySpider'])

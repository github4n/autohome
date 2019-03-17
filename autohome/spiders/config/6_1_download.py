#!/usr/bin/python
# coding=utf-8
import re

import scrapy
from scrapy.cmdline import execute

from autohome.spiders.utils.PathUtils import PathUtils
from autohome.spiders.utils.DbUtils import DbUtils


class DownloadSpider(scrapy.Spider):
    # 爬虫名称
    name = '6_download'

    def __init__(self):
        PathUtils.initDir()  # 初始化文件夹
        dbUtils = DbUtils('5_spec')  # 加载数据库
        self.queryItems = dbUtils.select(None)  # 查询数据

    def start_requests(self):
        for item in self.queryItems:
            url = 'https://car.autohome.com.cn/config/spec/%s.html' % item['id']
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        webId = re.search('(\d+)', response.url).group(0)
        html = response.body.decode(response.encoding)
        rootPath = PathUtils.getRootPath()
        path = rootPath + "\\output\\1_originHtml\\%s.html" % webId
        with  open(path, "w", encoding="utf-8") as f:
            f.write(html)


if __name__ == "__main__":
    execute(['scrapy', 'crawl', '6_download'])

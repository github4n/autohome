#!/usr/bin/python
# coding=utf-8
import json
import logging
import re

import scrapy
from scrapy.cmdline import execute

from autohome.items import CommentItem
from autohome.spiders.utils.DbUtils import DbUtils
from autohome.spiders.utils.ExcelUtils import ExcelUtils

logger = logging.getLogger(__name__)


class NewsAllSpider(scrapy.Spider):
    name = 'news_3_comment'

    def __init__(self):
        # 数据库操作
        dbUtils = DbUtils('news_2_article')
        # self.queryItems = dbUtils.select({"id": "930991"})

    def start_requests(self):
        # for item in self.queryItems:
        # yield scrapy.Request(url=url, callback=self.parse, meta={"id": item['id']})
        url = url = 'https://reply.autohome.com.cn/api/comments/show.json?count=50&page=1&id=930949&appid=1&datatype=jsonp&order=0&replyid=0'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = CommentItem()
        data = re.search('{(.*)}', response.text).group(0)
        response_json = json.loads(data)
        # 评论总条数
        commentCount = response_json['commentcount']
        # 获取当前接收到评论的条数
        try:
            receiveLen = response.meta['receiveLen']
            receiveLen = receiveLen + len(response_json['commentlist'])
        except:
            receiveLen = len(response_json['commentlist'])

        # 解析评论数据
        for jsonItem in response_json['commentlist']:
            item['content'] = jsonItem['RContent']
            item['userImgUrl'] = "https:" + jsonItem['RUserHeaderImage']
            item['userName'] = jsonItem['RMemberName']
            item['time'] = jsonItem['replydate']
            item['floor'] = jsonItem['RFloor']
            item['id'] = re.search('&id=([0-9]*)', response.url).group(1)
            yield item
        # 判断是否还有下一页数据
        if receiveLen < commentCount:
            try:
                page = response.meta['page']
                page = page + 1
            except:
                page = 2
            url = 'https://reply.autohome.com.cn/api/comments/show.json?count=50&page={}&id={}&appid=1&datatype=jsonp&order=0&replyid=0'.format(page, item['id'])
            yield scrapy.Request(url=url, callback=self.parse, meta={"page": page, "receiveLen": receiveLen})


if __name__ == "__main__":
    execute(['scrapy', 'crawl', 'news_3_comment'])
    dbUtils = DbUtils('news_3_comment')
    queryItems = dbUtils.select(None)
    excelUtils = ExcelUtils()
    excelUtils.generateExcel('news', 'news_3_comment', list(queryItems))

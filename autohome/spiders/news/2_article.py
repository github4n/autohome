#!/usr/bin/python
# coding=utf-8
import json
import logging
import re

import scrapy
from scrapy.cmdline import execute

from autohome.items import ArticleItem
from autohome.spiders.utils.DbUtils import DbUtils

logger = logging.getLogger(__name__)


class NewsAllSpider(scrapy.Spider):
    name = 'news_2_article'

    def __init__(self):
        # 数据库操作
        dbUtils = DbUtils('news_1_main')
        self.queryItems = dbUtils.selectByPage(None, 0, 100)
        # self.queryItems = dbUtils.select({id: "927060"})

    def start_requests(self):
        for item in self.queryItems:
            yield scrapy.Request(url=item['url'], callback=self.parse)
        # url = 'https://www.autohome.com.cn/drive/201903/927060.html#pvareaid=102624'
        # yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # 阅读全文url
        readAll = response.xpath('//*[@class="athm-page__info"]/a[@class="athm-page__readall"]/@href').extract()
        if readAll:
            # 如果有阅读全文就解析全文
            url = "https://www.autohome.com.cn" + readAll[0]
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            # 没有就解析当前页面
            article_item = ArticleItem()
            # 当前url
            article_item['url'] = response.url

            # 文章定位
            article_item['location'] = self.getLocation(response.xpath('//div[@class="breadnav fn-left"]//text()').extract())

            # 文章信息
            article_item['title'] = response.xpath('//*[@id="articlewrap"]/h1//text()').extract()[0].strip()
            try:
                article_item['writer'] = response.xpath('//div[@class="article-info"]/div[@class="name"]/a/text()').extract()[0]
            except:  # 当前作者没有详情
                article_item['writer'] = response.xpath('//div[@class="article-info"]/div[@class="name"]/text()').extract()[0]
            article_item['pub_time'] = response.xpath('//div[@class="article-info"]/span[1]/text()').extract()[0].strip()
            article_item['type'] = response.xpath('//div[@class="article-info"]/span[@class="type"]/text()').extract()[0]
            article_item['fromUrl'] = response.xpath('//div[@class="article-info"]/span[@class="source"]/a/text()').extract()[0]

            # 文章部分
            article_item['content'] = response.xpath('//div[@id="articleContent"]').extract()[0]
            article_item['photo'] = response.xpath('//div[@id="articleContent"]//img/@src').extract()
            article_item['tag'] = response.xpath('//div[@class="marks"]/a/text()').extract()[0]
            article_item['tag_link'] = response.xpath('//div[@class="marks"]/a/@href').extract()[0]

            # 评论
            article_item['comment'] = "https:" + response.xpath(' //*[@id="reply-all-btn1"]/@href').extract()[0]

            articleId = re.search('/([0-9]*)[\.-]', response.url).group(1)
            article_item['id'] = articleId
            # 请求评论的数量
            countUrl = 'http://reply.autohome.com.cn/api/QueryComment/CountsByObjIds?_appid=cms&appid=1&dataType=json&objids={}'.format(articleId)
            yield scrapy.Request(url=countUrl, callback=self.articleCommentNum, meta={"item": article_item})

    # 获取评论的数量
    def articleCommentNum(self, response):
        article_item = response.meta['item']
        response_json = json.loads(response.text)
        article_item['comment_num'] = response_json['result']['objcounts'][0]['replycountall']
        yield article_item

    # 解析当前所在位置
    def getLocation(self, originList):
        locationList = []
        for item in originList:
            if len(item.strip()) > 0:
                locationList.append(item.strip())
        tmp = ''
        for i in range(1, len(locationList) - 1):
            tmp = tmp + locationList[i] + '->'

        return locationList[0] + tmp + locationList[-1]


if __name__ == "__main__":
    execute(['scrapy', 'crawl', 'news_2_article'])

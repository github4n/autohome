#!/usr/bin/python
# coding=utf-8


import scrapy
from scrapy.cmdline import execute

from autohome.items import ArticleShortItem


class NewsAllSpider(scrapy.Spider):
    name = 'news_1_main'
    start_urls = ['http://www.autohome.com.cn/all/']

    def parse(self, response):
        print(response.url)
        article_short_item = ArticleShortItem()
        for four_part_article in response.xpath('//ul[@class="article"]'):
            for each_short_article in four_part_article.xpath('.//li'):
                # 判断文章的url是否为空，将url是空的抛弃，解析非空的页面
                if each_short_article.xpath('.//a/@href').extract():
                    article_short_item['url'] = "https:" + each_short_article.xpath('.//a/@href').extract()[0]
                    article_short_item['pic'] = "https:" + each_short_article.xpath('.//img/@src').extract()[0]
                    article_short_item['title'] = each_short_article.xpath('.//h3/text()').extract()[0]
                    article_short_item['publicTime'] = each_short_article.xpath('.//span[@class="fn-left"]/text()').extract()[0]
                    article_short_item['readNum'] = each_short_article.xpath('.//span[@class="fn-right"]//em[1]/text()').extract()[0]
                    article_short_item['shortContent'] = ''.join(each_short_article.xpath('.//p/text()').extract()).strip()
                    yield article_short_item

        # 请求下一页
        next_url_part = response.xpath('//div[@id="channelPage"]/a[@class="page-item-next"]/@href').extract()[0]
        if next_url_part != '':
            article_next_url = 'http://www.autohome.com.cn{}'.format(next_url_part)
            yield scrapy.http.Request(article_next_url, callback=self.parse)


if __name__ == "__main__":
    execute(['scrapy', 'crawl', 'news_1_main'])

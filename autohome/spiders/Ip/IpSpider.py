import scrapy
from scrapy.cmdline import execute

from autohome.items import IpProxyItem


# 爬取西刺Ip代理
class IpSpider(scrapy.Spider):
    name = 'ip_pool'
    start_urls = ['https://www.xicidaili.com/wt/']

    def parse(self, response):
        table = response.xpath('//table[@id="ip_list"]')
        for tr in table.xpath('./tr'):
            item = IpProxyItem()
            try:
                item['ip'] = tr.xpath('./td[2]/text()').extract()[0]
                item['port'] = tr.xpath('./td[3]/text()').extract()[0]
                item['type'] = tr.xpath('./td[6]/text()').extract()[0]
            except:
                continue
            yield item


if __name__ == "__main__":
    execute(['scrapy', 'crawl', 'ip_pool'])

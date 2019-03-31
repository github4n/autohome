import scrapy
from scrapy.cmdline import execute


# IP查询 主要用于ip代理测试
class IpQuerySpider(scrapy.Spider):
    name = 'IpQuery'

    def start_requests(self):
        for i in range(5):
            url = 'http://2019.ip138.com/ic.asp'
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print(response.body.decode(response.encoding))


if __name__ == "__main__":
    execute(['scrapy', 'crawl', 'IpQuery'])

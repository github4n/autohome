# -*- coding: utf-8 -*-
import codecs
import json

import requests
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter


class JsonWithEncodingPipeline(object):
    def __init__(self, file_name=None):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def open_spider(self, spider):
        self.file.write("[\n")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"  # 确保中文显示正常
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()

    # # 通过该方法创建该对象
    @classmethod
    def from_crawler(cls, crawler):
        file_name = crawler.settings.get('FILE_NAME')  # 获取setting.py信息
        return cls(file_name)


# 调用 scrapy 提供的 json exporter 导出 json 文件
class JsonExporterPipeline(object):

    def __init__(self):
        self.file = open('questions_exporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)  # 输出中文格式
        self.exporter.start_exporting()

    # 关闭资源
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    # 将 Item 实例导出到 json 文件
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# 保存数据到MongoDb
class CrawlDataToMongoPipeline(object):
    collection = None

    def __init__(self, host, port, dataBase):
        self.client = MongoClient(host=host, port=port)  # 创建连接对象client
        self.db = self.client[dataBase]

    def open_spider(self, spider):
        collection = spider.name
        self.collection = self.db[collection]

    def close_spider(self, spider):
        self.client.close()  # 关闭数据库

    def process_item(self, item, spider):
        job_info = dict(item)  # item转换为字典格式
        self.collection.insert(job_info)  # 将item写入mongo
        return item

    # # 通过该方法创建该对象
    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('MONGO_IP')  # 获取setting.py信息
        port = crawler.settings.get('MONGO_PORT')  # 获取setting.py信息
        dataBase = crawler.settings.get('MONGO_DATABASE')  # 获取setting.py信息
        return cls(host, port, dataBase)


# 检查Ip是否可用
class IpProxyPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'ip_pool':
            ip = item['ip'] + ':' + item['port']

            if self.proxyIpCheck(ip) is False:
                raise DropItem('ip: %s 不可用' % ip)
            else:
                print('ip：' + ip + '可用，存入数据库！')
        return item

    def proxyIpCheck(self, ip):
        proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
        try:
            response = requests.get('http://www.baidu.com/', proxies=proxies, timeout=1)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False

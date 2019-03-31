# -*- coding: utf-8 -*-

import random

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

# userAgent轮换
from autohome.spiders.utils.DbUtils import DbUtils


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agent_list=crawler.settings.get('USER_AGENT_LIST'))

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = user_agent
        # print(user_agent)


# IP代理
class ProxyMiddleware(object):
    def __init__(self, ip_pool):
        self.ip_pool = ip_pool

    @classmethod
    def from_crawler(cls, crawler):
        dbUtils = DbUtils('ip_pool')
        queryItems = dbUtils.select(None)
        return cls(ip_pool=list(queryItems))

    def process_request(self, request, spider):
        item = random.choice(self.ip_pool)
        request.meta['proxy'] = '%s://%s:%s' % (item['type'].lower(), item['ip'], item['port'])

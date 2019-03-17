# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BrandItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    bfirstletter = scrapy.Field()
    logo = scrapy.Field()


class FactoryItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    firstLetter = scrapy.Field()
    parentId = scrapy.Field()


class SeriesItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    firstLetter = scrapy.Field()
    seriesState = scrapy.Field()
    seriesOrder = scrapy.Field()
    parentId = scrapy.Field()


class YearItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    parentId = scrapy.Field()


class SpecItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    state = scrapy.Field()
    minPrice = scrapy.Field()
    maxPrice = scrapy.Field()
    parentId = scrapy.Field()


class ConfigItem(scrapy.Item):
    _id = scrapy.Field()  # mongoDb 的_id
    id = scrapy.Field()  # 当前爬取的页面id
    config = scrapy.Field()
    option = scrapy.Field()
    bag = scrapy.Field()


class ArticleShortItem(scrapy.Item):
    """
    文章首页的缩略信息
    """
    # 文章url
    url = scrapy.Field()
    # 文章首页缩略图
    pic = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 文章发布时间
    publicTime = scrapy.Field()
    # 文章阅读数量
    readNum = scrapy.Field()
    # 文章缩略前面篇幅
    shortContent = scrapy.Field()


class ArticleItem(scrapy.Item):
    """
    详细文章页面信息
    """
    # 文章id
    id = scrapy.Field()
    # 文章url
    url = scrapy.Field()
    # 当前位置
    location = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 文章作者
    writer = scrapy.Field()
    # 发布时间
    pub_time = scrapy.Field()
    # 文章类型
    type = scrapy.Field()
    # 文章来源
    fromUrl = scrapy.Field()
    # 详细文章
    content = scrapy.Field()
    # 文章图片
    photo = scrapy.Field()
    # 文章标签
    tag = scrapy.Field()
    # 文章标签连接
    tag_link = scrapy.Field()
    # 文章评论连接
    comment = scrapy.Field()
    # 文章评论数量
    comment_num = scrapy.Field()


class CommentItem(scrapy.Item):
    # 文章id
    id = scrapy.Field()
    # 评论用户名
    userName = scrapy.Field()
    # 用户头像url
    userImgUrl = scrapy.Field()
    # 当前楼层
    floor = scrapy.Field()
    # 评论内容
    content = scrapy.Field()
    # 评论时间
    time = scrapy.Field()

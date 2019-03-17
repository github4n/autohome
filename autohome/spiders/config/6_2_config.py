#!/usr/bin/python
# coding=utf-8
import json
import os
import re

from selenium import webdriver

from autohome.items import ConfigItem
from autohome.spiders.utils.DbUtils import DbUtils
from autohome.spiders.utils.PathUtils import PathUtils

if __name__ == "__main__":

    # 数据库操作
    dbUtils = DbUtils('6_config')
    # 当前项目根目录
    rootPath = PathUtils.getRootPath()
    # 注入的Js
    injectJs = ("let rules = '';"
                "document.createElement = function() {"
                "      return {"
                "              sheet: {"
                "                      insertRule: function(rule, i) {"
                "                              if (rules.length == 0) {"
                "                                      rules = '#' + rule;"
                "                              } else {"
                "                                      rules = rules + '#' + rule;"
                "                              }"
                "                      }"
                "              }"
                "      }"
                "};"
                "document.head = {};"
                "document.head.appendChild = function() {};")

    # 加载selenium驱动
    browser = webdriver.Chrome('%s\\chromedriver.exe' % rootPath)

    files = os.listdir(rootPath + "/output/1_originHtml")
    for fileName in files:
        webId = re.search('(\d+)', fileName.title()).group(0)
        with open(rootPath + "/output/1_originHtml/" + fileName, "r", encoding="utf-8") as f:
            responseBody = f.read()

        # 2 抽取Js 并注入js 并保存为文件
        originJs = re.findall('(\(function\([a-zA-Z]{2}.*?_\).*?\(document\);)', responseBody)
        tmpStr = injectJs
        for item in originJs:
            tmpStr = tmpStr + item
        finalJs = "<script>%s document.write(rules);</script>" % tmpStr
        with  open(rootPath + "/output/2_decodeJs/%s.html" % webId, "a", encoding="utf-8") as f:
            f.write(finalJs)

        # 3 使用selenium输出上一步的js结果
        browser.get("file:///%s/output/2_decodeJs/%s.html" % (rootPath, webId))
        spanList = browser.find_element_by_tag_name('body').text

        # 4 提取原网页关键js数据对象
        config = re.search('var config = (.*);', responseBody).group(1)
        option = re.search('var option = (.*);', responseBody).group(1)
        bag = re.search('var bag = (.*);', responseBody).group(1)

        # 5 替换原网页关键js数据对象--》生成解密后的js对象
        classList = re.findall('hs_kw\w*', spanList)
        contentList = re.findall('[\u4e00-\u9fa5]+', spanList)
        for i in range(0, contentList.__len__()):
            config = config.replace("<span class='%s'></span>" % classList[i], contentList[i])
            option = option.replace("<span class='%s'></span>" % classList[i], contentList[i])
            bag = bag.replace("<span class='%s'></span>" % classList[i], contentList[i])

        # 6 对json内部过滤
        config = json.loads(config)['result']['paramtypeitems']
        option = json.loads(option)['result']['configtypeitems']
        bag = json.loads(bag)['result']['bagtypeitems']

        # 7 将数据存入数据库
        item = ConfigItem()
        item['id'] = webId
        item['config'] = config
        item['option'] = option
        item['bag'] = bag
        dbUtils.insert(item)

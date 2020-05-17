# -*- coding: utf-8 -*-
import scrapy
import re
from baidunews.items import BaidunewsItem
from scrapy.http import Request


class N1Spider(scrapy.Spider):
    name = 'n1'
    allowed_domains = ['baidu.com']
    start_urls = ['https://news.baidu.com/widget?id=LocalNews&ajax=json']
    allId = []
    allUrl = []
    fh = open("F:/python_practice/scrapy练习/baidunews/baidunews/spiders/demo.md", "r", encoding="utf-8")
    pat = 'h.*?id=(.*?)&'
    for i in fh:
        thisData = re.compile(pat).findall(i)
        # print(thisData)
        if len(thisData) != 0:
            allId.append(thisData[0])
        # else:
        #     allId.append(i)
    # print(allId)
    for j in range(0, len(allId)):
        thisUrl = 'https://news.baidu.com/widget?id=' + allId[j] + '&ajax=json'
        allUrl.append(thisUrl)
    # print(allUrl)

    def parse(self, response):
        for m in range(0, len(self.allUrl)):
            print("第" + str(m) + "个栏目")
            yield Request(self.allUrl[m], callback=self.next)

    def next(self, response):
        data = response.body.decode("utf-8", "ignore")
        pat = '"url":"(.*?)"'
        pat1 = '"m_url":"(.*?)"'
        url1 = re.compile(pat, re.S).findall(data)
        url2 = re.compile(pat1, re.S).findall(data)
        if len(url1) != 0:
            url = url1
        else:
            url = url2
        # print(url)
        for i in range(0, len(url)):
            thisUrl = re.sub("\\\/", "/", url[i])
            print(thisUrl)
            yield Request(thisUrl, callback=self.next1)

    def next1(self, response):
        item = BaidunewsItem()
        item["link"] = response.url
        item["title"] = response.xpath("/html/head/title/text()").extract()
        item["content"] = response.body
        yield item


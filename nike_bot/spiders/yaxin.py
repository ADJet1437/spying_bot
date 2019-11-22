# -*- coding: utf-8 -*-
import scrapy
import re


class YaxinSpider(scrapy.Spider):
    name = 'yaxin'
    allowed_domains = ['yaxin.yunkushop.com/']
    start_urls = ['http://yaxin.yunkushop.com/']

    def parse(self, response):
        print(response.url)
        feature_links = response.xpath('//a[contains(@href, "feature")]/@href').extract()
        for feature_link in feature_links:
            match = re.findall(r'feature/d+', feature_link)
            if match:
                url = match[0]
                siid = match.split('/')[1]
                self.insert_link_to_db(conn=None, url=url, siid=siid)
            else:
                print("Warning, no feature links")

    def insert_link_to_db(self, conn, url, siid):
        pass

    def send_email(self):
        pass
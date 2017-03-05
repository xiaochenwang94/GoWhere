# -*- coding:utf-8 -*-

import scrapy
import time
from foursqSpider.items import FoursqspiderItem

class FsqSpider(scrapy.Spider):
    name = 'foursquare'
    allow_domains = ['foursquare.com']
    start_urls = ['https://foursquare.com/v/madison-square-garden/4ae6363ef964a520aba521e3?tipsSort=popular']

    def parse(self, response):
        item = FoursqspiderItem()
        for sel in response.xpath('//*[@id="tipsList"]/li'):
            item['date'] = sel.xpath('div[@class="tipContents"]/div[1]/span[2]/text()').extract()
            item['userName'] = sel.xpath('div[@class="tipContents"]/div[1]/span[1]/a/text()').extract()
            item['content'] = sel.xpath('div[@class="tipContents"]/div[2]/text()').extract()
            yield item
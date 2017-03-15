# -*- coding:utf-8 -*-

import scrapy
import time
from foursqSpider.items import FoursqspiderItem

class FsqSpider(scrapy.Spider):
    name = 'foursquare'
    allow_domains = ['foursquare.com']
    start_urls = ['https://foursquare.com/v/madison-square-garden/4ae6363ef964a520aba521e3']
    # start_urls = ['https://foursquare.com/v/madison-square-park/40b68100f964a5207d001fe3?tipsPage=%s&tipsSort=popular' % i for i in xrange(1,9)]
    def __init__(self):
        self.index = 0
    def parse(self, response):
        item = FoursqspiderItem()
        for sel in response.xpath('//ul[@id="tipsList"]/li'):
            item['date'] = sel.xpath('div[@class="tipContents"]/div[1]/span[2]/text()').extract()
            item['user_name'] = sel.xpath('div[@class="tipContents"]/div[1]/span[1]/a/text()').extract()
            item['content'] = sel.xpath('div[@class="tipContents"]/div[2]/text()').extract()
            yield item
        self.index += 1
        next_page = response.xpath('//*[@id="tipsContainer"]/div/div/a[@data-index="%s"]/@href' % self.index).extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse)
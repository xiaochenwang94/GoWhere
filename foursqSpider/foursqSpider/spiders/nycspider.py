import scrapy
from foursqSpider.items import NycItem
import logging
class NycSpider(scrapy.Spider):
    name = 'nycspider'
    allow_domains = ['foursquare.com']
    start_urls = ['https://foursquare.com/explore?mode=url&near=New%20York%2C%20NY%2C%20United%20States&nearGeoId=72057594043056517']

    def __init__(self):
        self.index = 0
        self.base_url = 'https://foursquare.com'

    def parse(self, response):
        for sel in response.xpath('//*[@id="results"]/ul/li[4]'):
            url = sel.xpath('div[2]/div[1]/div[1]/div/div[1]/h2/a/@href').extract_first()
            full_url = self.base_url + str(url) + '?tipsSort=popular'
            # print(full_url)
            yield scrapy.Request(full_url, callback = self.parse_location)


    def parse_location(self, response):
        item = NycItem()
        for sel in response.xpath('//ul[@id="tipsList"]/li'):
            item['date'] = sel.xpath('div[@class="tipContents"]/div[1]/span[2]/text()').extract_first()
            item['user_name'] = sel.xpath('div[@class="tipContents"]/div[1]/span[1]/a/text()').extract_first()
            item['content'] = sel.xpath('div[@class="tipContents"]/div[2]/text()').extract()
            item['location_name'] = sel.xpath('//*[@id="container"]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/h1/text()').extract_first()
            yield item
        self.index += 1
        next_page = response.xpath('//*[@id="tipsContainer"]/div/div/a[@data-index="%s"]/@href' % self.index).extract_first()
        logging.debug(next_page)
        if next_page is not None:
            next_page = self.base_url + str(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback = self.parse_location)
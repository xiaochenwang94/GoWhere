from scrapy import cmdline
import os

cmdline.execute("scrapy crawl foursquare -t csv -o madison.csv".split())
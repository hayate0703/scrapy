# -*- coding: utf-8 -*-
import scrapy

from familug.items import FamilugItem, time_convert
from scrapy.loader import ItemLoader
from scrapy.http import Request


class FmlSpider(scrapy.Spider):
    name = "fml"
    allowed_domains = ["familug.org"]
    start_urls = (
        'http://www.familug.org/',
    )


    def parse(self, response):
    	# Get the next page and yield Request
    	next_selector = response.xpath(
    		'//*[@class="blog-pager-older-link"]/@href')
    	for url in next_selector.extract():
    		yield Request(url)

    	# Get URL in page and yield Request
    	url_selector = response.xpath('//*[@class="post hentry"]//h3//@href')
    	for url in url_selector.extract():
    		yield Request(url, callback=self.parse_item)


    def parse_item(self, response):
    	item = FamilugItem()
    	
    	item['title'] = response.xpath(
    		'//*[@class="post-title entry-title"]/text()').extract()[0]
    	item['date'] = time_convert(response.xpath(
    		'//*[@class="date-header"]/span/text()').extract()[0])
    	item['author'] = response.xpath(
    		'//*[@itemprop="author"]/a/span/text()').extract()[0]
    	item['content'] = response.xpath(
    		'//*[@class="post-body entry-content"]/node()').extract()
    	item['url'] = response.url
        return item

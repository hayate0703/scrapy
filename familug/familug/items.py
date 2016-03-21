# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import time
from scrapy.item import Item, Field


class FamilugItem(Item):
    # Primary Fields
    title = Field()
    date = Field()
    content = Field()
    author = Field()
    #Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    pass

def time_convert(n):
	'''
	Convert string time into ISO format
	More doccument: https://docs.python.org/2/library/time.html#time.strptime
	'''
	convert = time.strptime(n, "%A, %d %B %Y")
	return time.strftime("%Y-%m-%d", convert)